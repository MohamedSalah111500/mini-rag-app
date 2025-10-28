from fastapi import FastAPI, APIRouter ,Depends,UploadFile,status
from fastapi.responses import JSONResponse
import aiofiles
import os
from controllers import DataController, ProjectController
from helpers.config import Settings, get_settings
from models.enums.responses import ResponseType

data_router = APIRouter( 
            prefix="/api/v1/data",
            tags=["api_v1","data"]
            )


@data_router.post("/upload/{project_id}")
async def update_data(project_id: str,file: UploadFile, 
                      app_setting: Settings = Depends(get_settings)):
    is_valid = DataController().validate_uploaded_file(file=file)
    if(is_valid == False):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": ResponseType.FILE_TYPE_NOT_SUPPORTED.value})
        
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = os.path.join(project_dir_path,file.filename)
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        while chank := await file.read(app_setting.FILE_DEFAULT_CHUNK_SIZE):
            await out_file.write(chank)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": ResponseType.FILE_UPLOADED_SUCCESSFULLY.value})
  

