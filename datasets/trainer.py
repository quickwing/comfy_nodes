from trl import GRPOConfig
from trl import GRPOTrainer
import traceback
class GRPOTrainingArgsNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "max_seq_length": ("INT", {"default": 1024}),
                "max_prompt_length": ("INT", {"default": 256}),
            },
            "optional": {
                "learning_rate": ("FLOAT", {"default": 5e-6}),
                "adam_beta1": ("FLOAT", {"default": 0.9}),
                "adam_beta2": ("FLOAT", {"default": 0.99}),
                "weight_decay": ("FLOAT", {"default": 0.1}),
                "warmup_ratio": ("FLOAT", {"default": 0.1}),
                "lr_scheduler_type": ("STRING", {"default": "cosine"}),
                "optim": ("STRING", {"default": "paged_adamw_8bit"}),
                "logging_steps": ("INT", {"default": 1}),
                "per_device_train_batch_size": ("INT", {"default": 1}),
                "gradient_accumulation_steps": ("INT", {"default": 1}),
                "num_generations": ("INT", {"default": 6}),
                "num_train_epochs": ("INT", {"default": 1}),
                "max_steps": ("INT", {"default": 250}),
                "save_steps": ("INT", {"default": 250}),
                "max_grad_norm": ("FLOAT", {"default": 0.1}),
                # "report_to": ("STRING", {"default": "none"}),
                "output_dir": ("STRING", {"default": "outputs"}),
            }
        }

    RETURN_TYPES = ("TRAINING_ARGS",)
    RETURN_NAMES = ("training_args",)
    FUNCTION = "__call__"
    CATEGORY = "sim/training"

    def __call__(self, *args, **kwargs):
        max_seq_length = kwargs.pop("max_seq_length")
        max_prompt_length = kwargs.get("max_prompt_length", 256)
        kwargs["max_completion_length"] = max_seq_length - max_prompt_length
        return (GRPOConfig(**kwargs),)

class GRPOTrainerTrainNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "tokenizer": ("TOKENIZER",),
                "training_args": ("TRAINING_ARGS",),
                "reward_funcs": ("REWARD_FUNCTION_LIST",),
                "train_dataset": ("DATASET",),
            },
            "optional": {
                "callbacks": ("CALLBACK_LIST",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "__call__"
    CATEGORY = "sim/training"

    def __call__(self, *args, **kwargs):
        model = kwargs["model"]
        tokenizer = kwargs["tokenizer"]
        training_args = kwargs["training_args"]
        reward_funcs = kwargs["reward_funcs"]
        dataset = kwargs["train_dataset"]
        callbacks = kwargs.get("callbacks", [])
        # dataset = dataset.map(
        #     lambda x: {"tokens" : tokenizer.apply_chat_template(x["prompt"], add_generation_prompt = True, tokenize = True)},
        # )
        dataset = dataset.map(
            lambda x: {"truth" : x["label"]},
        )
        dataset = dataset.remove_columns(["label", "text"])
        try:
            trainer = GRPOTrainer(
                model=model,
                processing_class=tokenizer,
                reward_funcs=reward_funcs,
                args=training_args,
                train_dataset=dataset,
                #callbacks=callbacks if callbacks else None,
            )
            trainer.train()
            return ("Training complete.",)
        except Exception as e:
            tb = traceback.format_exc()
            return (f"Training failed:\n{tb}",)


# class WandBLoggerNode:
#     def __init__(self):
#         super().__init__()

#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "optional": {
#                 "project": ("STRING", {"default": "comfyui-project", "label": "Project Name"}),
#                 "run_name": ("STRING", {"default": "", "label": "Run Name"}),
#                 "tags": ("STRING", {"default": "", "label": "Comma-separated tags"}),
#             }
#         }

#     RETURN_TYPES = ("LOGGER",)
#     RETURN_NAMES = ("wandb_logger",)
#     FUNCTION = "__call__"
#     CATEGORY = "sim/logging"

#     def __call__(self, *args, **kwargs):
#         project = kwargs.get("project", "comfyui-project")
#         entity = kwargs.get("entity", None)
#         run_name = kwargs.get("run_name", None)
#         tags = [t.strip() for t in kwargs.get("tags", "").split(",") if t.strip()]

#         try:
#             wandb.init(
#                 project=project,
#                 name=run_name or None,
#                 tags=tags or None,
#             )
#             return (wandb,)
#         except Exception as e:
#             return (f"Logger failed: {str(e)}",)

from transformers import TrainerCallback
import torch

class TextGenerationCallbackNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "tokenizer": ("TOKENIZER",),
                "dataset": ("DATASET",),
                "key": ("STRING", {"default": "text", "multiline": False}),
                "seed_system_prompt": ("STRING", {"default": "", "multiline": True}),
                "top_p": ("FLOAT", {"default": 0.9}),
                "temperature": ("FLOAT", {"default": 0.8}),
                "max_length": ("INT", {"default": 12000}),
                "interval": ("INT", {"default": 500}),
            },
            "optional": {
                "CALLBACK_LIST": ("CALLBACK_LIST",),
            }
        }

    RETURN_TYPES = ("CALLBACK_LIST",)
    RETURN_NAMES = ("callbacks",)
    FUNCTION = "__call__"
    CATEGORY = "sim/callbacks"

    def __call__(self, *args, **kwargs):
        model = kwargs["model"]
        tokenizer = kwargs["tokenizer"]
        dataset = kwargs["dataset"]
        key = kwargs["key"]
        top_p = kwargs["top_p"]
        temperature = kwargs["temperature"]
        max_length = kwargs["max_length"]
        interval = kwargs["interval"]

        class TextGenerationCallback(TrainerCallback):
            def __init__(self):
                self.tokenizer = tokenizer
                self.model = model
                self.max_length = max_length
                self.interval = interval
                self.top_p = top_p
                self.temperature = temperature

            def on_step_end(self, args, state, control, **kwargs):
                if state.global_step % self.interval == 0:
                    print("args!!!!", args)
                    print("kwargs!!!!", kwargs)
                    print("\n--- Text Generation Callback ---")
                    for seed_text in self.seed_texts[:3]:
                        input_ids = self.tokenizer(seed_text, return_tensors="pt").input_ids.to(self.model.device)
                        with torch.no_grad():
                            output_ids = self.model.generate(
                                input_ids=input_ids,
                                max_length=self.max_length,
                                do_sample=True,
                                top_p=self.top_p,
                                temperature=self.temperature,
                                pad_token_id=self.tokenizer.eos_token_id,
                            )
                        output_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
                        print(f"Seed: {seed_text}\nOutput: {output_text}\n")

        cb = TextGenerationCallback()
        callbacks = kwargs.get("CALLBACK_LIST", [])
        if not isinstance(callbacks, list):
            callbacks = [callbacks]
        callbacks.append(cb)
        return (callbacks,)
