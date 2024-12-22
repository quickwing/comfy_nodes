import os
from pydub import AudioSegment
import json
from openai import OpenAI

class OpenaiFixJsonPrepAudio:
    def __init__(self):
        pass

    def get_audio_file(self, audio_output_path, input_text):

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        speech_file_path = os.path.join(audio_output_path)
        response = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",#, 'nova'
        input=input_text
        )

        response.stream_to_file(speech_file_path)

        audio = AudioSegment.from_file(speech_file_path)
        print('generated audio file: ', audio.duration_seconds, ' ', audio_output_path)
        return audio.duration_seconds

    def generate_final_json_and_audio(self, input_json, path_to_output, fol_for_audio_output):
        ''' 
        Input: input_json: str or dict
        It must be a path or a dictionary
        '''
        if type(input_json) == str:
            with open(input_json, 'r') as f:
                data = json.load(f)
        else:
            data = input_json
        data["source"] = ""
        data["h"] = 1920
        data["w"] = 1080

        for i in range(len(data['slides'])):
            print(data['slides'][i])
            if 'slideNarration' in data['slides'][i]:
                text = data['slides'][i]['slideNarration']
                len_sec = self.get_audio_file(os.path.join(fol_for_audio_output, f'speech_{i}.mp3'), text)
                len_frames = int(len_sec * 30) + 30
                data['slides'][i]['audioSrc'] = f'speech_{i}.mp3'
                data['slides'][i]['duration'] = len_frames

        with open(path_to_output, 'w+') as f:
            json.dump(data, f, indent=4)
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json": ("STRING", {"forceInput": True}),
                "output_folder": ("STRING", {"default": "/home/sghumman/ML/out/public"}),
            },
        }
 
    RETURN_TYPES = ("STRING","STRING", )
    RETURN_NAMES = ("output_json","first_description", )
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/audio/openai_json_to_audio"
 
    def __call__(self, *args, **kwargs):
        ''' 
        make audio
        '''
        my_json = kwargs['json']
        print(my_json)
        my_json = json.loads(my_json)
        self.generate_final_json_and_audio(my_json, os.path.join(kwargs["output_folder"], "output_json.json"), kwargs["output_folder"])
        return (json.dumps(my_json, indent=4),my_json["slides"][0]["imageDescription"], )