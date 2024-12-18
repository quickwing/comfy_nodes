class GenericPrompt:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "system": ("STRING", {"default": "You are a helpful assisstant"}),
                "instruction": ("STRING", {"default": "", "multiline": True}, ),
                "text": ("STRING", {"forceInput": True}),
            },
        }
 
    RETURN_TYPES = ("MESSAGES",)
    RETURN_NAMES = ("messages",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/lm/prompts"
 
    def __call__(self, *args, **kwargs):
        ''' 
        generate a generic prompt
        '''
        messages = []
        messages.append({"role": "system", "content": kwargs["system"]})
        user_message = f'''
        {kwargs["instruction"]}
        {kwargs["text"]}
        '''
        messages.append({"role": "user", "content": user_message})

        return (messages,)