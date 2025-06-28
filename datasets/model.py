from unsloth import FastLanguageModel
import torch

class LoadUnslothModelNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": ("STRING", {"default": "meta-llama/meta-Llama-3.1-8B-Instruct", "multiline": False}),
                "max_seq_length": ("STRING", {"default": "1024", "multiline": False}),
                "lora_rank": ("STRING", {"default": "32", "multiline": False}),
                "load_in_4bit": ("BOOLEAN", {"default": True}),
                "gpu_memory_utilization": ("STRING", {"default": "0.6", "multiline": False}),
            }
        }

    RETURN_TYPES = ("MODEL", "TOKENIZER")
    RETURN_NAMES = ("model", "tokenizer")
    FUNCTION = "__call__"
    CATEGORY = "sim/models"

    def __call__(self, *args, **kwargs):
        model_name = kwargs.get("model_name")
        max_seq_length = int(kwargs.get("max_seq_length"))
        lora_rank = int(kwargs.get("lora_rank"))
        load_in_4bit = kwargs.get("load_in_4bit")
        gpu_memory_utilization = float(kwargs.get("gpu_memory_utilization"))

        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=max_seq_length,
            load_in_4bit=load_in_4bit,
            fast_inference=False,
            max_lora_rank=lora_rank,
            gpu_memory_utilization=gpu_memory_utilization,
        )

        model = FastLanguageModel.get_peft_model(
            model,
            r=lora_rank,
            target_modules=[
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj",
            ],
            lora_alpha=lora_rank,
            #use_gradient_checkpointing="unsloth",
        )

        return (model, tokenizer)
