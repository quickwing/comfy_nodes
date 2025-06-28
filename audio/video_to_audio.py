from subprocess import check_output

class VideoToAudio:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path_to_vid": ("STRING", {"default":"C:\\ML\\"}),
                "output_audio_path": ("STRING", {"default":"C:\\ML\\"}),
            },
        }
 
    RETURN_TYPES = ("AUDIO_PATH",)
    RETURN_NAMES = ("audio_file_path",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/generate_datasets/videos"
 
    def __call__(self, *args, **kwargs):

        path_to_vid = kwargs["path_to_vid"]
        output_audio_path = kwargs["output_audio_path"]
        check_output(f"ffmpeg -i {path_to_vid} -vn -ar 44100 -ac 2 -ab 192k -f wav {output_audio_path}", shell=True).decode()
        
        return (output_audio_path,)