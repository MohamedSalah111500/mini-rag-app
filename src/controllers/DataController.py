
from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        
        self.size_scale = 1048576 # convert to 1MB 
    def validate_uploaded_file(self,file: UploadFile):
        
        if(file.content_type not in self.app_settings.FILE_ALLOWED_TYPES):
            return False
        
        if(file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale):
            return False
        
        return True
    
    def generate_unique_file_name(self,original_file_name: str,project_id:str):
       random_file_name = self.generate_random_string()
       project_path = ProjectController().get_project_path(project_id=project_id)