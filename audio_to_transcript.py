import torchaudio
from .audio_diar import DiartationTranscriber
import os
from torchaudio import transforms

class AudioToTranscript:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path_to_audio": ("AUDIO_PATH", {"default":"C:\\ML\\"}),
                "language": ("STRING", {"default":"french"}),
            },
        }
 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("transcript",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/generate_datasets/audio"
 
    def __call__(self, *args, **kwargs):
        language = kwargs["language"]
        path_to_audio = kwargs["path_to_audio"]
        diar = DiartationTranscriber(None, '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')

        waveform, sample_rate = torchaudio.load(path_to_audio, normalize=True)
        if sample_rate != 16000:
            transform = transforms.Resample(sample_rate, 16000)
            waveform = transform(waveform)
            print(f"resampling from SR : {sample_rate} to 16000")
        torchaudio.save("test.wav", waveform, 16000)
        out = diar("test.wav", language=language)
        os.remove("test.wav")
        
        return (out,)