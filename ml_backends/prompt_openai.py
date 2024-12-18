from openai import OpenAI

class PromptOpenAI:
    def __init__(self):
        self.client = OpenAI()
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("STRING", {"default": "gpt-4o-mini"}),
                "messages": ("MESSAGES", {"forceInput": True}),
            },
        }
 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/lm/backend"
 
    def __call__(self, *args, **kwargs):
        ''' 
        Prompt openai
        '''

        completion = self.client.chat.completions.create(
            model=kwargs["model"],
            messages=kwargs["messages"],
        )

        print(completion.choices[0].message)
        response = completion.choices[0].message.content

        return (response,)