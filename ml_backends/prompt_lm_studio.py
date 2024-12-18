import requests
import json

class PromptLMStudio:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("STRING", {"default": "llama"}),
                "messages": ("MESSAGES", {"forceInput": True}),
            },
        }
 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/lm/backend"
    def prompt_lm_studio(messages):
        headers = {
                    "Content-Type": "application/json"
                    }
        # The JSON data payload
        data1 = {
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": -1,
                "stream": False
                }

        # Making the POST request to the local server
        response = requests.post('http://localhost:1234/v1/chat/completions', headers=headers, data=json.dumps(data1))
        resp_content1 = json.loads(response.text)["choices"][0]["message"]["content"]
        return resp_content1
    
    def __call__(self, *args, **kwargs):
        ''' 
        Prompt LMStudio
        '''
        resp = self.prompt_lm_studio(kwargs["messages"])

        return (resp,)