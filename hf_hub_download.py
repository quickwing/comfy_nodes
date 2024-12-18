#incomplete

import json
import requests
from huggingface_hub import snapshot_download
import os

class PromptLmStudio:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "hf_token": ("STRING", {"default": os.environ.get("HF_TOKEN")}),
                "messages": ("STRING", {"default": "huggingface repo"}),
            },
        }
 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/scraping/prompt_lm_studio"
 
    def __call__(self, *args, **kwargs):
        ''' 
        Iterate over folder in path
        and provide a list of paths to files in subfolders
        as a list of strings
        '''
        html = self.driver.find_elements(By.CLASS_NAME, kwargs['div'])
        html = html[0].get_attribute('innerText')
        return (html,)

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