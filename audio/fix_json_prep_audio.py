from TTS.api import TTS
import torch
import os
import uuid
from pydub import AudioSegment
import json

class FixJsonPrepAudio:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json": ("STRING", {"forceInput": True}),
                'speaker_file_pth': ("STRING", {"default": "/home/sghumman/ML/monorepo/test.wav"}),
                "output_folder": ("STRING", {"default": "/home/sghumman/ML/out/public"}),
            },
        }
 
    RETURN_TYPES = ("STRING","STRING", )
    RETURN_NAMES = ("output_json","first_description", )
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/audio/TTS"
 
    def __call__(self, *args, **kwargs):
        ''' 
        make audio
        '''
        my_json = kwargs['json']

        print(my_json)
        my_json = json.loads(my_json)
        project = str(uuid.uuid4())
        for num, item in enumerate(my_json["slides"]):
            if "slideNarration" in item:
                narration = item["slideNarration"]
                output_file_name = f"voice{project}-{num}.wav"
                output_file_path = os.path.join(kwargs["output_folder"], output_file_name)
                tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

                # generate speech by cloning a voice using default settings
                tts.tts_to_file(text=narration,
                                file_path=output_file_path,
                                speaker_wav=kwargs["speaker_file_pth"],
                                language="en")
                audio = AudioSegment.from_file(output_file_path)
                print('generated audio file: ', audio.duration_seconds, ' ', output_file_path)
                len_frames = int(audio.duration_seconds * 30) + 30
                my_json['slides'][num]['audioSrc'] = output_file_name
                my_json['slides'][num]['duration'] = len_frames
        my_json["h"] = 1920
        my_json["w"] = 1080
        del tts
        torch.cuda.empty_cache()

        return (json.dumps(my_json, indent=4),my_json["slides"][0]["imageDescription"], )