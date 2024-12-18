from subprocess import check_output

class PopUpFile:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path_to_file": ("STRING", {"default":"C:\\ML\\"}),
            },
        }
 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path to file",)

    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/utils/save_text"
 
    def __call__(self, *args, **kwargs):
        path = kwargs["path_to_file"]
        check_output(f"notepad.exe {path}", shell=True).decode()
        
        return (path,)