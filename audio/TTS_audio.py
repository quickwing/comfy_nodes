from TTS.api import TTS
import torch

class TTSTextToWav:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"default": "this is a test"}),
                'speaker_file_pth': ("AUDIO_PATH", {"default": ""}),
                "output_file_pth": ("STRING", {"default": ""}),
            },
        }
 
    RETURN_TYPES = ("AUDIO_PATH",)
    RETURN_NAMES = ("output_file_pth",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/audio/TTS"
 
    def __call__(self, *args, **kwargs):
        ''' 
        make audio
        '''

        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

        # generate speech by cloning a voice using default settings
        tts.tts_to_file(text=kwargs["text"],
                        file_path=kwargs["output_file_pth"],
                        speaker_wav=kwargs["speaker_file_pth"],
                        language="en")

        del tts
        torch.cuda.empty_cache()

        return (kwargs['output_file_pth'],)