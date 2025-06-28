from unsloth import FastLanguageModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig, TaskType

class LoadQLoraModelNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": ("STRING", {
                    "default": "meta-llama/Llama-3.2-1B-Instruct",
                    "multiline": False,
                    "label": "Hugging Face Model Name"
                }),
                "quantization": (["4bit", "8bit"], {
                    "default": "8bit",
                    "label": "Quantization Type"
                }),
                "lora_rank": ("INT", {
                    "default": 16,
                    "min": 1,
                    "max": 128,
                    "label": "LoRA Rank"
                }),
                "lora_alpha": ("INT", {
                    "default": 32,
                    "min": 1,
                    "max": 256,
                    "label": "LoRA Alpha"
                }),
                "max_seq_length": ("INT", {
                    "default": 2048,
                    "min": 128,
                    "max": 16384,
                    "label": "Max Sequence Length"
                }),
            }
        }

    RETURN_TYPES = ("MODEL", "TOKENIZER",)
    RETURN_NAMES = ("model", "tokenizer",)
    FUNCTION = "__call__"
    CATEGORY = "sim/models"

    def __call__(self, *args, **kwargs):
        import torch
        model_name = kwargs["model_name"]
        quantization = kwargs["quantization"]
        lora_rank = kwargs["lora_rank"]
        lora_alpha = kwargs["lora_alpha"]
        max_seq_length = kwargs["max_seq_length"]

        bnb_config = BitsAndBytesConfig(
            load_in_8bit=(quantization == "8bit"),
            load_in_4bit=(quantization == "4bit"),
            # You can uncomment and customize these lines if needed
            # bnb_4bit_quant_type="nf4",
            # bnb_4bit_use_double_quant=True,
            # bnb_4bit_compute_dtype=torch.bfloat16,
        )

        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        tokenizer.model_max_length = max_seq_length
        tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )

        lora_config = LoraConfig(
            r=lora_rank,
            lora_alpha=lora_alpha,
            target_modules=[
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj",
            ],
            lora_dropout=0.05,
            bias="none",
            task_type=TaskType.CAUSAL_LM,
        )

        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()

        print("QLoRA model loaded!")
        return (model, tokenizer)


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
