import sys

from .generate_file_list import FolderToFiles
from .ml_backends.prompt_local import PromptLocal
from .ml_backends.prompt_openai import PromptOpenAI
from .ml_backends.prompt_lm_studio import PromptLMStudio
from .ml_backends.prompt_local_8bit import PromptLocal8Bit
# if sys.platform != 'win32':
#     from .audio.fix_json_prep_audio import FixJsonPrepAudio
#     from .audio.TTS_audio import TTSTextToWav
# from .audio.openai_fix_json_prep_audio import OpenaiFixJsonPrepAudio
# from .webdriver import GiveWebdriver
# from .prompt_templates.extract_article import ExtractArticle
from .prompt_templates.generic import GenericPrompt
# from .prompt_templates.generate_video_json import GenerateVideoJson
from .audio_to_transcript import AudioToTranscript
# from .audio.video_to_audio import VideoToAudio
from .utils.save_file import SaveText
from .prompt_templates.extract_question import ExtractQuestion
from .utils.open_file import OpenFile
from .utils.pop_up_file import PopUpFile
from .datasets.model import *
from .datasets.rewards import *
from .datasets.dataset import *
from .datasets.trainer import *
from dotenv import load_dotenv

load_dotenv()  #

NODE_CLASS_MAPPINGS = {
    "generate_image_paths_from_subfolders": FolderToFiles,
    # "web_driver_to_html": GiveWebdriver,
    "prompt local": PromptLocal,
    "prompt local 8bit": PromptLocal8Bit,
    # "extract_article": ExtractArticle,
    "generic_prompt": GenericPrompt,
    "prompt_openai": PromptOpenAI,
    "audio_to_transcript": AudioToTranscript,
    # "video_to_audio": VideoToAudio,
    'save_text': SaveText,
    'extract_question': ExtractQuestion,
    'read_file': OpenFile,
    'pop_up_file': PopUpFile,
    # 'generate_video_json': GenerateVideoJson,
    'prompt_lm_studio': PromptLMStudio,
    # "openai_fix_json_prep_audio": OpenaiFixJsonPrepAudio,
    "load_unsloth_model": LoadUnslothModelNode,
    "CorrectnessRewardNode": CorrectnessRewardNode,
    "IntRewardNode": IntRewardNode,
    "StrictFormatRewardNode": StrictFormatRewardNode,
    "SoftFormatRewardNode": SoftFormatRewardNode,
    "XMLCountRewardNode": XMLCountRewardNode,
    "ExtractHashAnswerNode": ExtractHashAnswerNode,
    "ExtractXMLAnswerNode": ExtractXMLAnswerNode,
    "FormatXMLAnswerNode": FormatXMLAnswerNode,
    "LiteralStringNode": LiteralStringNode,
    "ApplyStringFunctionsNode": ApplyStringFunctionsNode,
    "GRPOTrainingArgsNode": GRPOTrainingArgsNode,
    "GRPOTrainerTrainNode": GRPOTrainerTrainNode,
    "GSM8KDatasetNode": GSM8KDatasetNode, 
    "MapStringFunctionsNode": MapStringFunctionsNode,
    "LoadHuggingFaceDatasetNode": LoadHuggingFaceDatasetNode,
    "ConcatWithStringNode": ConcatWithStringNode, 
    "SampleDatasetNode": SampleDatasetNode,
    "ToPromptMessagesNode": ToPromptMessagesNode,
    "StructuredAnswerRewardNode": StructuredAnswerRewardNode,
    "TextGenerationCallbackNode": TextGenerationCallbackNode,
    "DatasetTrainTestSplitNode": DatasetTrainTestSplitNode,
    'CutStringAtEnd': CutStringAtEnd,
    "LoadQLoraModelNode": LoadQLoraModelNode,
    "FilterDatasetKeysNode": FilterDatasetKeysNode
}

# if sys.platform != 'win32':
#     NODE_CLASS_MAPPINGS["fix_json_prep_audio"] = FixJsonPrepAudio
#     NODE_CLASS_MAPPINGS["tts_text_to_wav"] = TTSTextToWav

 
# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "data": "Subfolders to Files",
}

__all__ = ["NODE_CLASS_MAPPINGS"]

''' 
LIST_OF_PATHS
LIST_OF_FILE_NAMES
MESSAGES
AUDIO_PATH
MODEL
TOKENIZER
STRING_FUNCTION_LIST
REWARD_FUNCTION_LIST
TRAINING_ARGS 
DATASET
'''
