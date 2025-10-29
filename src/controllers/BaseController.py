
from helpers.config import Settings, get_settings
import os
import random
import string

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir,"assets/files")
        
    def generate_random_string(self, length=12):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def clean_file_name(self, orig_file_name):
        return ''.join(e for e in orig_file_name if e.isalnum())