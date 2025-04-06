from fastapi import FastAPI, APIRouter ,Depends
from helpers.config import Settings, get_settings
base_router = APIRouter( 
            prefix="/api/v1",
            tags=["base"]
            )


@base_router.get("/")
async def read_root(app_setting: Settings = Depends(get_settings)):
    
    app_name= app_setting.APP_NAME
    app_version= app_setting.APP_VERSION
    
    return {"app_name": app_name, "app_version": app_version}
