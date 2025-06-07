#############################################################################################################################
###### FastAPI packages #####################################################################################################
from fastapi import APIRouter, Depends,UploadFile, File
#############################################################################################################################
###### Use cases ############################################################################################################
from scan.use_cases.get_image_result import GetImageResult
#############################################################################################################################
###### Repositories Implementation ##########################################################################################
from scan.infrastructure.repository.scan_image_repository_sql import ScanImageRepositorySQL
#############################################################################################################################
###### Dependencies #########################################################################################################
from scan.api.dependencies import user_dependency
from infrastructure.db.dependencies import db_dependency
#############################################################################################################################
###### Exceptions ###########################################################################################################
from core.exceptions.exceptions import ImageNotSupported, UnSupportedFormat, AppException
from core.exceptions.http_exceptions import HTTPImageNotSupported, HTTPUnsupportedFileFormat, HTTPFailedToFetchImages
#############################################################################################################################
#############################################################################################################################

router = APIRouter(
    prefix="/scan",
    tags=["ML model domain"]
)




@router.post("/scan-sample-image", status_code=200)
async def scan_sample_image(db: db_dependency, user: user_dependency, file: UploadFile = File(...)):
    try:
        repo = ScanImageRepositorySQL(db)
        use_case = GetImageResult(repo)
        result = await use_case.execute(user["id"], file)
        return result
    except ImageNotSupported:
        raise HTTPImageNotSupported()
    except UnSupportedFormat:
        raise HTTPUnsupportedFileFormat()
    except AppException:
        raise HTTPFailedToFetchImages()

        #will fix it later