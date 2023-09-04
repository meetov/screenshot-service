import fastapi
import pydantic
from starlette.responses import FileResponse

from crawler.process import ScreenshotCrawler
from crawler.package import ScreenshotPackage

app = fastapi.FastAPI()


class StartCrawlerRequest(pydantic.BaseModel):
    start_url: str
    url_limit: int


@app.get('/isalive')
async def health_check():
    return {'status': 'OK'}


@app.post('/screenshots/')
def start_crawler(request_body: StartCrawlerRequest):
    crawler = ScreenshotCrawler()
    return {"package_id": crawler.start(start_url=request_body.start_url, url_limit=request_body.url_limit)}


@app.get('/screenshots/{package_id}')
def get_screenshots(package_id: int):
    package = ScreenshotPackage.from_id(package_id=package_id)
    return package.get_files()


@app.get('/screenshots/{package_id}/file/{file_id}', response_class=FileResponse)
def get_screenshot(package_id: int, file_id: int):
    package = ScreenshotPackage.from_id(package_id=package_id)
    return package.get_file_path(file_id=file_id)
