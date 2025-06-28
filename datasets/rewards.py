class CorrectnessRewardNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {"optional": {"rewards": ("REWARD_FUNCTION_LIST",)}}

    RETURN_TYPES = ("REWARD_FUNCTION_LIST",)
    RETURN_NAMES = ("rewards",)
    FUNCTION = "__call__"
    CATEGORY = "sim/rewards"

    def __call__(self, *args, **kwargs):
        def extract_xml_answer(text):
            answer = text.split("<answer>")[-1]
            answer = answer.split("</answer>")[0]
            return answer.strip()

        def reward_func(prompts, completions, answer, **_):
            responses = [c[0]['content'] for c in completions]
            extracted = [extract_xml_answer(r) for r in responses]
            return [2.0 if r == a else 0.0 for r, a in zip(extracted, answer)]

        rewards = kwargs.get("rewards", [])
        if not isinstance(rewards, list): rewards = [rewards]
        rewards.append(reward_func)
        return (rewards,)

class IntRewardNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {"optional": {"rewards": ("REWARD_FUNCTION_LIST",)}}

    RETURN_TYPES = ("REWARD_FUNCTION_LIST",)
    RETURN_NAMES = ("rewards",)
    FUNCTION = "__call__"
    CATEGORY = "sim/rewards"

    def __call__(self, *args, **kwargs):
        def extract_xml_answer(text):
            return text.split("<answer>")[-1].split("</answer>")[0].strip()

        def reward_func(completions, **_):
            responses = [c[0]['content'] for c in completions]
            extracted = [extract_xml_answer(r) for r in responses]
            return [0.5 if r.isdigit() else 0.0 for r in extracted]

        rewards = kwargs.get("rewards", [])
        if not isinstance(rewards, list): rewards = [rewards]
        rewards.append(reward_func)
        return (rewards,)

import re

class StrictFormatRewardNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {"optional": {"rewards": ("REWARD_FUNCTION_LIST",)}}

    RETURN_TYPES = ("REWARD_FUNCTION_LIST",)
    RETURN_NAMES = ("rewards",)
    FUNCTION = "__call__"
    CATEGORY = "sim/rewards"

    def __call__(self, *args, **kwargs):
        pattern = r"^<reasoning>\n.*?\n</reasoning>\n<answer>\n.*?\n</answer>\n$"

        def reward_func(completions, **_):
            responses = [c[0]["content"] for c in completions]
            return [0.5 if re.match(pattern, r) else 0.0 for r in responses]

        rewards = kwargs.get("rewards", [])
        if not isinstance(rewards, list): rewards = [rewards]
        rewards.append(reward_func)
        return (rewards,)
class SoftFormatRewardNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {"optional": {"rewards": ("REWARD_FUNCTION_LIST",)}}

    RETURN_TYPES = ("REWARD_FUNCTION_LIST",)
    RETURN_NAMES = ("rewards",)
    FUNCTION = "__call__"
    CATEGORY = "sim/rewards"

    def __call__(self, *args, **kwargs):
        pattern = r"<reasoning>.*?</reasoning>\s*<answer>.*?</answer>"

        def reward_func(completions, **_):
            responses = [c[0]["content"] for c in completions]
            return [0.5 if re.match(pattern, r) else 0.0 for r in responses]

        rewards = kwargs.get("rewards", [])
        if not isinstance(rewards, list): rewards = [rewards]
        rewards.append(reward_func)
        return (rewards,)
class XMLCountRewardNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {"optional": {"rewards": ("REWARD_FUNCTION_LIST",)}}

    RETURN_TYPES = ("REWARD_FUNCTION_LIST",)
    RETURN_NAMES = ("rewards",)
    FUNCTION = "__call__"
    CATEGORY = "sim/rewards"

    def __call__(self, *args, **kwargs):
        def count_xml(text):
            count = 0.0
            if text.count("<reasoning>\n") == 1: count += 0.125
            if text.count("\n</reasoning>\n") == 1: count += 0.125
            if text.count("\n<answer>\n") == 1:
                count += 0.125
                count -= len(text.split("\n</answer>\n")[-1])*0.001
            if text.count("\n</answer>") == 1:
                count += 0.125
                count -= (len(text.split("\n</answer>")[-1])-1)*0.001
            return count

        def reward_func(completions, **_):
            contents = [c[0]["content"] for c in completions]
            return [count_xml(c) for c in contents]

        rewards = kwargs.get("rewards", [])
        if not isinstance(rewards, list): rewards = [rewards]
        rewards.append(reward_func)
        return (rewards,)
class ExtractHashAnswerNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "functions": ("STRING_FUNCTION_LIST",)
            }
        }

    RETURN_TYPES = ("STRING_FUNCTION_LIST",)
    RETURN_NAMES = ("functions",)
    FUNCTION = "__call__"
    CATEGORY = "sim/string_functions"

    def __call__(self, *args, **kwargs):
        def extract_hash_answer(text: str) -> str:
            if "####" not in text:
                return ""
            return text.split("####")[1].strip()

        functions = kwargs.get("functions", [])
        if not isinstance(functions, list):
            functions = [functions]
        functions.append(extract_hash_answer)
        return (functions,)
class ExtractXMLAnswerNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "functions": ("STRING_FUNCTION_LIST",)
            }
        }

    RETURN_TYPES = ("STRING_FUNCTION_LIST",)
    RETURN_NAMES = ("functions",)
    FUNCTION = "__call__"
    CATEGORY = "sim/string_functions"

    def __call__(self, *args, **kwargs):
        def extract_xml_answer(text: str) -> str:
            answer = text.split("<answer>")[-1]
            answer = answer.split("</answer>")[0]
            return answer.strip()

        functions = kwargs.get("functions", [])
        if not isinstance(functions, list):
            functions = [functions]
        functions.append(extract_xml_answer)
        return (functions,)
class FormatXMLAnswerNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "reasoning": ("STRING", {"multiline": True, "default": "my reasoning"}),
                "answer": ("STRING", {"multiline": False, "default": "42"})
            },
            "optional": {
                "functions": ("STRING_FUNCTION_LIST",)
            }
        }

    RETURN_TYPES = ("STRING_FUNCTION_LIST",)
    RETURN_NAMES = ("functions",)
    FUNCTION = "__call__"
    CATEGORY = "sim/string_functions"

    def __call__(self, *args, **kwargs):
        reasoning = kwargs["reasoning"]
        answer = kwargs["answer"]

        def xml_formatter(_: str = "") -> str:
            return f"<reasoning>\n{reasoning}\n</reasoning>\n<answer>\n{answer}\n</answer>\n"

        functions = kwargs.get("functions", [])
        if not isinstance(functions, list):
            functions = [functions]
        functions.append(xml_formatter)
        return (functions,)

class LiteralStringNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("STRING", {"multiline": True, "default": ""})
            },
            "optional": {
                "functions": ("STRING_FUNCTION_LIST",)
            }
        }

    RETURN_TYPES = ("STRING_FUNCTION_LIST",)
    RETURN_NAMES = ("functions",)
    FUNCTION = "__call__"
    CATEGORY = "sim/string_functions"

    def __call__(self, *args, **kwargs):
        value = kwargs["value"]

        def identity(_: str = "") -> str:
            return value

        functions = kwargs.get("functions", [])
        if not isinstance(functions, list):
            functions = [functions]
        functions.append(identity)
        return (functions,)
class ApplyStringFunctionsNode:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "functions": ("STRING_FUNCTION_LIST",)
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result",)
    FUNCTION = "__call__"
    CATEGORY = "sim/string_functions"

    def __call__(self, *args, **kwargs):
        text = kwargs["text"]
        funcs = kwargs["functions"]

        try:
            for func in funcs:
                text = func(text)
            return (text,)
        except Exception as e:
            return (f"Error: {str(e)}",)
