from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By

from selenium import webdriver

class GiveWebdriver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://www.lapresse.ca')
        time.sleep(5)

    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default":"https://www.lapresse.ca"}),
                'div': ("STRING", {"default":"mainContent"}),
            },
        }
 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("html",)
 
    FUNCTION = "__call__"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "sim/scraping/webdriver"
 
    def __call__(self, *args, **kwargs):
        ''' 
        Iterate over folder in path
        and provide a list of paths to files in subfolders
        as a list of strings
        '''
        html = self.driver.find_elements(By.CLASS_NAME, kwargs['div'])
        html = html[0].get_attribute('innerText')
        return (html,)