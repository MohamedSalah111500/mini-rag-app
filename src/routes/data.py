from fastapi import FastAPI, APIRouter ,Depends,UploadFile,status
from fastapi.responses import JSONResponse
import aiofiles
import os
import logging
from controllers import DataController,ProjectController,ProcessController
from helpers.config import Settings, get_settings
from models.enums.ResponsesEnum import ResponseType
from .schema import ProcessRequest

ProcessRequest
logger = logging.getLogger("uvicorn.error")
data_controller = DataController()
data_router = APIRouter( 
            prefix="/api/v1/data",
            tags=["api_v1","data"]
            )


@data_router.post("/upload/{project_id}")
async def update_data(project_id: str,file: UploadFile, 
                      app_setting: Settings = Depends(get_settings)):
    
    is_valid = data_controller.validate_uploaded_file(file=file)
    if(is_valid == False):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": ResponseType.FILE_TYPE_NOT_SUPPORTED.value})
   
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path , file_id = data_controller.generate_unique_filepath(
        orig_file_name = file.filename,
        project_id=project_id
        )
  
    try:   
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_setting.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
            
    except Exception as e:
        logger.error(f"Error while uploading file {file.filename} to {file_path}", e)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": ResponseType.FILE_UPLOADED_FAILED.value})
        
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": ResponseType.FILE_UPLOADED_SUCCESSFULLY.value,
                                 "file_id":file_id
                                 }
                        )


@data_router.post("/process/{project_id}")
async def process_data(project_id: str,process_request: ProcessRequest):
  file_id = process_request.file_id
  chunk_size = process_request.chunk_size
  overLab_size = process_request.overLab_size
  
  process_controller = ProcessController(project_id=project_id)
  file_content = process_controller.get_file_content(file_id=file_id)
  file_chunks = process_controller.process_file_content(file_content=file_content,
                                                        file_id=file_id,
                                                        chunk_size=chunk_size,
                                                        overLab_size=overLab_size)
  
  if(file_chunks is None or len(file_chunks) == 0):
      return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": ResponseType.PROCESSING_FAILED.value})
      
  return JSONResponse(status_code=status.HTTP_200_OK,
                      content={"message": ResponseType.PROCESSING_SUCCESSFULLY.value, "chunks": file_chunks})

