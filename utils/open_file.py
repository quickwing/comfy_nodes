class OpenFile:
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
    RETURN_NAMES = ("file as string",)

    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/utils/save_text"
 
    def __call__(self, *args, **kwargs):
        path = kwargs["path_to_file"]
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        return (text,)