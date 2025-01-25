import subprocess
import os

class VideoToAudio:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                'video_file_path': ("STRING", {"default": ""}),
                "output_file_pth": ("STRING", {"default": ""}),
            },
        }
 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_file_pth",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/audio/video_to_audio"
 
    def __call__(self, *args, **kwargs):
        ''' 
        make audio
        '''
        video_file = kwargs["video_file_path"]
        subprocess.call(["ffmpeg", "-y", "-i", video_file, kwargs["output_file_pth"]], 
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)

        return (kwargs['output_file_pth'],)