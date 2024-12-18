class SaveText:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path_to_save": ("STRING", {"default":"C:\\ML\\"}),
                "text": ("STRING", {"forceInput": True}),
            },
        }
 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path_saved",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/utils/save_text"
 
    def __call__(self, *args, **kwargs):
        path = kwargs["path_to_save"]
        text = kwargs["text"]

        with open(path, "w+", encoding="utf-8") as f:
            f.write(text)
        
        return (path,)