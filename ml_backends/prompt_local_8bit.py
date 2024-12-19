from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
import torch

class PromptLocal8Bit:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_path": ("STRING", {"default": "meta-llama/Llama-3.1-8B-Instruct"}),
                'max_new_tokens': ("INT", {"default": 12000 }),
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
        Prompt local model
        '''
        model_id = kwargs["model_path"]
        messages = kwargs["messages"]

        quantization_config = BitsAndBytesConfig(load_in_8bit=True)

        model = AutoModelForCausalLM.from_pretrained(
            model_id, 
            quantization_config=quantization_config
        )
        tokenizer = AutoTokenizer.from_pretrained(model_id)

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer= tokenizer,
            device_map="auto",
        )

        tokenized_sentence = tokenizer.tokenize(str(messages))
        print('number of tokens : ', len(tokenized_sentence)) # here is the tokenized length

        terminators = [
            pipe.tokenizer.eos_token_id,
        ]
        outputs = pipe(
            messages,
            max_new_tokens=kwargs["max_new_tokens"],
            eos_token_id=terminators,
        )
        print('outputs:', outputs)
        response = outputs[0]["generated_text"][-1]["content"]
        print('response:', response)

        del pipe
        torch.cuda.empty_cache()

        return (response,)