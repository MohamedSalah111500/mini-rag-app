from typing import Optional
from pydantic import BaseModel

class ProcessRequest(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100
    overLab_size: Optional[int] = 20
    do_reset: Optional[int] = 0