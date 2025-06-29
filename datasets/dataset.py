from datasets import load_dataset, Dataset, DatasetDict
import re

class FilterDatasetKeysNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dataset": ("DATASET",),
                "keys": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "label": "Comma-separated keys or single key"
                }),
                "remove": ("BOOLEAN", {
                    "default": True,
                    "label": "Remove keys (True) or keep only (False)"
                }),
            }
        }

    RETURN_TYPES = ("DATASET",)
    RETURN_NAMES = ("filtered_dataset",)
    FUNCTION = "__call__"
    CATEGORY = "sim/datasets"

    def __call__(self, *args, **kwargs):
        dataset = kwargs["dataset"]
        keys = kwargs["keys"]
        remove = kwargs["remove"]

        if isinstance(dataset, Dataset):
            return (dataset,)  # Single split dataset, return as-is

        if not isinstance(dataset, DatasetDict):
            return ("Error: Input is not a DatasetDict.",)

        key_list = [k.strip() for k in keys.split(",") if k.strip()]

        if len(key_list) == 1 and "," not in keys:
            key = key_list[0]
            if key in dataset:
                return (dataset[key],)
            else:
                return (f"Error: Key '{key}' not found in dataset.",)

        if remove:
            kept_keys = [k for k in dataset.keys() if k not in key_list]
        else:
            kept_keys = [k for k in dataset.keys() if k in key_list]

        filtered = {k: dataset[k] for k in kept_keys}
        return (DatasetDict(filtered),)


class GSM8KDatasetNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "split": ("STRING", {"default": "train"})
            }
        }

    RETURN_TYPES = ("DATASET",)
    RETURN_NAMES = ("dataset",)
    FUNCTION = "__call__"
    CATEGORY = "sim/datasets"

    def __call__(self, *args, **kwargs):
        split = kwargs.get("split", "train")

        SYSTEM_PROMPT = """\
Respond in the following format:
<reasoning>
...
</reasoning>
<answer>
...
</answer>
"""

        def extract_hash_answer(text: str):
            if "####" not in text:
                return None
            return text.split("####")[1].strip()

        try:
            data = load_dataset('openai/gsm8k', 'main')[split]  # type: ignore
            data = data.map(lambda x: {
                'prompt': [
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': x['question']}
                ],
                'answer': extract_hash_answer(x['answer'])
            })  # type: ignore
            return (data,)
        except Exception as e:
            raise RuntimeError(f"Failed to load or process dataset: {str(e)}")

from datasets import Dataset

class MapStringFunctionsNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "functions": ("STRING_FUNCTION_LIST",),
                "dataset": ("DATASET",),
                "input_key": ("STRING", {"default": "text"}),
                "output_key": ("STRING", {"default": "processed_text"}),
            }
        }

    RETURN_TYPES = ("DATASET","STRING_FUNCTION_LIST",)
    RETURN_NAMES = ("processed_dataset","functions", )
    FUNCTION = "__call__"
    CATEGORY = "sim/datasets"

    def __call__(self, *args, **kwargs):
        functions = kwargs["functions"]
        dataset: Dataset = kwargs["dataset"]
        input_key: str = kwargs["input_key"]
        output_key: str = kwargs["output_key"]

        # Compose functions
        def composed_fn(s: str) -> str:
            for f in functions:
                s = f(s)
            return s

        # Apply map
        def apply_map(batch):
            batch[output_key] = composed_fn(batch[input_key])
            return batch

        mapped_dataset = dataset.map(apply_map)
        return (mapped_dataset,functions,)

from datasets import load_dataset

from huggingface_hub import login
from datasets import load_dataset

class LoadHuggingFaceDatasetNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dataset_name": ("STRING", {"default": "openai/gsm8k"}),
            },
            "optional": {
                "subset_name": ("STRING", {"default": ""}),
                "split": ("STRING", {"default": "train"}),
                "do_split": ("BOOLEAN", {"default": True}),
                "hf_token": ("STRING", {"default": "", "multiline": False, "label": "Hugging Face Token"}),
            }
        }

    RETURN_TYPES = ("DATASET",)
    RETURN_NAMES = ("dataset",)
    FUNCTION = "__call__"
    CATEGORY = "sim/datasets"

    def __call__(self, *args, **kwargs):
        dataset_name = kwargs["dataset_name"]
        subset_name = kwargs.get("subset_name", "").strip()
        split = kwargs.get("split", "train")
        do_split = kwargs.get("do_split", True)
        hf_token = kwargs.get("hf_token", "").strip()

        if hf_token:
            login(token=hf_token, add_to_git_credential=False)

        if subset_name:
            dataset = load_dataset(dataset_name, subset_name)
        else:
            dataset = load_dataset(dataset_name)

        if do_split:
            return (dataset[split],)
        else:
            return (dataset,)

class CutStringAtEnd:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "max_number": ("INT", {"default": 1048, "label": "Max number for the string"}),
            },
            "optional": {
                "functions": ("STRING_FUNCTION_LIST",)
            }
        }

    RETURN_TYPES = ("STRING_FUNCTION_LIST",)
    RETURN_NAMES = ("cut_string_at_end_function",)
    FUNCTION = "__call__"
    CATEGORY = "sim/functions"

    def __call__(self, *args, **kwargs):
        max_number = kwargs["max_number"]
        functions = kwargs.get("functions", [])
        def cut_fn(s: str) -> str:
            ret = ' '.join(s.split(" ")[:max_number])
            return ret
        functions.append(cut_fn)
        return (functions,)

class ConcatWithStringNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "fixed_string": ("STRING", {"default": "", "multiline": True, "label": "String to add"}),
                "prepend": ("BOOLEAN", {"default": False, "label": "Prepend instead of append?"}),
            },
            "optional": {
                "functions": ("STRING_FUNCTION_LIST",)
            }
        }

    RETURN_TYPES = ("STRING_FUNCTION_LIST",)
    RETURN_NAMES = ("concat_function",)
    FUNCTION = "__call__"
    CATEGORY = "sim/functions"

    def __call__(self, *args, **kwargs):
        fixed_string = kwargs["fixed_string"]
        prepend = kwargs["prepend"]
        functions = kwargs.get("functions", [])
        def concat_fn(s: str) -> str:
            return fixed_string + s if prepend else s + fixed_string
        if not isinstance(functions, list):
            functions = [functions]
        functions.append(concat_fn)
        return (functions,)

class SampleDatasetNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dataset": ("DATASET",),
            },
            "optional": {
                "index": ("STRING", {"default": "", "label": "Index (as string)"}),
                "key": ("STRING", {"default": "", "label": "Key (e.g., 'train')"}),
            }
        }

    RETURN_TYPES = ("ANY",)
    RETURN_NAMES = ("value",)
    FUNCTION = "__call__"
    CATEGORY = "sim/datasets"

    def __call__(self, *args, **kwargs):
        dataset = kwargs["dataset"]
        index = kwargs.get("index", "").strip()
        key = kwargs.get("key", "").strip()

        if key:
            try:
                return (dataset[key],)
            except Exception as e:
                return (f"Error: invalid key '{key}' - {str(e)}",)

        if index:
            try:
                i = int(index)
                return (dataset[i],)
            except Exception as e:
                return (f"Error: invalid index '{index}' - {str(e)}",)

        return ("Error: Either 'key' or 'index' must be set.",)

class ToPromptMessagesNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "system_prompt": ("STRING", {"default": "You are a helpful tutor.", "multiline": True, "label": "System Prompt"}),
            },
            "optional": {
                "functions": ("STRING_FUNCTION_LIST",),
            }
        }

    RETURN_TYPES = ("STRING_FUNCTION_LIST",)
    RETURN_NAMES = ("functions",)
    FUNCTION = "__call__"
    CATEGORY = "sim/functions"

    def __call__(self, *args, **kwargs):
        system_prompt = kwargs["system_prompt"]
        functions = kwargs.get("functions", [])

        def to_prompt_messages(s: str) -> list:
            return [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": s}
            ]

        if not isinstance(functions, list):
            functions = [functions]
        functions.append(to_prompt_messages)

        return (functions,)

class StructuredAnswerRewardNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "rewards": ("REWARD_FUNCTION_LIST",)
            }
        }

    RETURN_TYPES = ("REWARD_FUNCTION_LIST",)
    RETURN_NAMES = ("rewards",)
    FUNCTION = "__call__"
    CATEGORY = "sim/rewards"

    def __call__(self, *args, **kwargs):
        rewards = kwargs.get("rewards", [])
        if not isinstance(rewards, list):
            rewards = [rewards]

        def reward_func(completions, **kw):
            def extract(xml, tag):
                match = re.search(fr"<{tag}>(.*?)</{tag}>", xml, re.DOTALL)
                return match.group(1).strip() if match else ""

            scores = []
            for num, comp in enumerate(completions):
                text = comp[0]["content"]
                reasoning = extract(text, "reasoning")
                confidence = extract(text, "confidence")
                answer = extract(text, "answer")

                try:
                    confidence = float(confidence)
                    answer = float(answer)
                    ground_truth = float(kw["truth"][num])
                except:
                    scores.append(0.0)
                    print("Failed with completions: ", completions)
                    continue

                confidence = max(0.0, min(1.0, confidence))  # Clamp
                error = abs(ground_truth - answer)
                base_score = max(0.0, 10.0 - error)  # Reward if close

                # Confidence scaling
                if confidence >= 0.7:
                    accuracy_reward = base_score if error < 0.5 else -5.0  # Penalize overconfident wrong answers
                elif confidence >= 0.3:
                    accuracy_reward = base_score * (1.0 - confidence) + base_score * confidence * (1.0 - error / 10)
                else:
                    # Low confidence: modest reward but only if not too wrong
                    accuracy_reward = base_score * 0.5 if error < 3.0 else 0.0

                # Reasoning length reward
                word_count = len(reasoning.split())
                reasoning_score = min(10.0, word_count / 10.0)

                total_score = accuracy_reward + reasoning_score
                scores.append(total_score)

            return scores

        rewards.append(reward_func)
        return (rewards,)

from datasets import DatasetDict

class DatasetTrainTestSplitNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dataset": ("DATASET",),
                "test_size": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 1.0}),
                "shuffle": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": 42}),
            }
        }

    RETURN_TYPES = ("DATASET", "DATASET")
    RETURN_NAMES = ("train_dataset", "test_dataset")
    FUNCTION = "__call__"
    CATEGORY = "sim/datasets"

    def __call__(self, *args, **kwargs):
        dataset = kwargs["dataset"]
        test_size = kwargs["test_size"]
        shuffle = kwargs["shuffle"]
        seed = kwargs["seed"]

        try:
            split = dataset.train_test_split(test_size=test_size, shuffle=shuffle, seed=seed)
            return (split["train"], split["test"])
        except Exception as e:
            raise RuntimeError(f"Failed to split dataset: {str(e)}")

class RenameDatasetKeyNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dataset": ("DATASET",),
                "in_key": ("STRING", {"default": "text", "label": "Input Key"}),
                "out_key": ("STRING", {"default": "renamed_text", "label": "Output Key"}),
            }
        }

    RETURN_TYPES = ("DATASET",)
    RETURN_NAMES = ("dataset",)
    FUNCTION = "__call__"
    CATEGORY = "sim/datasets"

    def __call__(self, *args, **kwargs):
        dataset = kwargs["dataset"]
        in_key = kwargs["in_key"]
        out_key = kwargs["out_key"]

        def rename_key(batch):
            batch[out_key] = batch[in_key]
            del batch[in_key]
            return batch

        renamed_dataset = dataset.map(rename_key)
        return (renamed_dataset,)