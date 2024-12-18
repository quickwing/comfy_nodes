from pyannote.audio import Pipeline
import torch
import os
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pydub import AudioSegment
import numpy as np
import unicodedata as ud

class DiartationTranscriber:
    def __init__(self, cache_dir, hf_token):
        self.pipeline = Pipeline.from_pretrained(
          "pyannote/speaker-diarization-3.1",
          use_auth_token=hf_token)
        if torch.cuda.is_available():
            device = torch.device("cuda:0")
        else:
            device = torch.device("cpu")
            
        self.pipeline = self.pipeline.to(device)



        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        model_id = "openai/whisper-large-v3"
        
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True, cache_dir=cache_dir
        )
        self.model.to(device)
        
        self.processor = AutoProcessor.from_pretrained(model_id, cache_dir=cache_dir)
        
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=1,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
        )
                
    def gen_diaration(self, path_to_file):
        diarization = self.pipeline(path_to_file)
        with open(os.path.join("rttm.txt"), "w") as rttm:
            diarization.write_rttm(rttm)
        
    def __call__(self,  path_to_file, language=None):
        self.gen_diaration(path_to_file)
        with open('rttm.txt') as f:
            lines = f.readlines()
        os.remove("rttm.txt")
        starts = []
        ends = []
        speakers = []
        last_speaker=""
        for lin in lines:
            lin = lin.split(' ')
            duration1 = float(lin[4])
            start = float(lin[3]) * 1000
            end = start + (float(lin[4]) * 1000)
            if len(starts)>0:
                cur_duration = end - starts[-1]
            else:
                cur_duration = 0
            if cur_duration > 30000:
                last_speaker = ""
            if duration1 > 0.5:
                if lin[7] != last_speaker:
                    starts.append(start)
                    ends.append(end)
                    speakers.append(lin[7])
                    last_speaker = lin[7]
                else:
                    start = float(lin[3]) * 1000
                    end = start + (float(lin[4]) * 1000)
                    ends[-1] = end
        latin_letters= {}
        
        def is_latin(uchr):
            try: return latin_letters[uchr]
            except KeyError:
                 return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))
        
        def only_roman_chars(unistr):
            return all(is_latin(uchr)
                   for uchr in unistr
                   if uchr.isalpha()) # isalpha suggested by John Machin
        
        dialogues = []
        last_speaker = ""
        a = AudioSegment.from_wav(path_to_file)
        a = a.set_channels(1)

        print(starts)
        print(ends)
        print(speakers)

        for num, person in enumerate(speakers):
            star = starts[num]
            en = ends[num]
            b = a[star:en]
            # b = b.set_frame_rate(16000)
            ar = np.array(b.get_array_of_samples())
            b.export("audio_segment.wav", format="wav")
            print(ar.shape[0]/16000)
            if language==None:
                out = self.pipe("audio_segment.wav")
            else:
                out = self.pipe("audio_segment.wav", generate_kwargs={"language": language})
            print(out)
            os.remove('audio_segment.wav')
            for chunk in out['chunks']:
                if only_roman_chars(chunk['text']):
                    dialogue = person + ": " + chunk['text']
                    dialogues.append(dialogue)
                    print(chunk['text'])
        return "\n".join(dialogues)
                
