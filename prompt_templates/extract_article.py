class ExtractArticle:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "html": ("STRING", {"forceInput": True}),
            },
        }
 
    RETURN_TYPES = ("MESSAGES",)
    RETURN_NAMES = ("messages",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/lm/prompts"
 
    def __call__(self, *args, **kwargs):
        ''' 
        Prompt local model
        '''
        messages = []
        messages.append({"role": "system", "content": "You are a helpful assistant"})
        user_message = f'''
        I will provide the extracted text from a news website. Can you extract the text of the main article from the provied text?
        Exclude words linking to other articles, links and any other irrelevant text.
        Please reply with the extracted text verbatim in its entirety.
        Your extracted text will be part of a larger pipeline. Please only provide the extracted text. 
        Do not say anything before or after the extracted text such as 'The extracted text is:' or 'Here is the extracted text:' etc.
        Here is the html:
        {kwargs["html"]}
        '''
        messages.append({"role": "user", "content": user_message})

        return (messages,)