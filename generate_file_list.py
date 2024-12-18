import tqdm
import os

class FolderToFiles:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default":"C:\\ML\\"}),
                "ignore_folders": ("STRING", {"default":"black,redbust"}),
            },
        }
 
    RETURN_TYPES = ("LIST_OF_PATHS","LIST_OF_FILE_NAMES",'INT')
    RETURN_NAMES = ("file_paths","file_names",'data_len')
 
    FUNCTION = "generate_file_list"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/generate_datasets/images"
 
    def generate_file_list(self, *args, **kwargs):
        ''' 
        Iterate over folder in path
        and provide a list of paths to files in subfolders
        as a list of strings
        '''

        ignore_fols = kwargs["ignore_folders"].split(",")
        origin_fol = kwargs["path"]
        file_paths = []
        file_names = []
        for fol in tqdm.tqdm(os.listdir(origin_fol)):
            if os.path.isdir(os.path.join(origin_fol, fol)):
                if fol not in ignore_fols:
                    for file in os.listdir(os.path.join(origin_fol, fol)):
                        if '.mp4' not in file:
                            file_paths.append(os.path.join(origin_fol, fol, file))
                            file_names.append(f"{fol}_-_{file}")
        len_files = len(file_paths)
        return (file_paths,file_names,len_files,)
 
 
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
# NODE_CLASS_MAPPINGS = {
#     "generate_image_paths_from_subfolders": FolderToFiles
# }
 
# # A dictionary that contains the friendly/humanly readable titles for the nodes
# NODE_DISPLAY_NAME_MAPPINGS = {
#     "data": "Subfolders to Files",
# }
