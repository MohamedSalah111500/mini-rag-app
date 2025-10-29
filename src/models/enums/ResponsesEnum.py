from enum import Enum

class ResponseType(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_IS_EXCEEDED = "file_size_is_exceeded"
    FILE_UPLOADED_SUCCESSFULLY = "file uploaded successfully"
    FILE_UPLOADED_FAILED = "file_uploaded_failed"
    PROCESSING_FAILED = "processing_failed"
    PROCESSING_SUCCESSFULLY = "processing_successfully"