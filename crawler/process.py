import abc
from crawler.crawler_tasks import start_crawl
from crawler.package import ScreenshotPackage


class CrawlerProcess(abc.ABC):
    @abc.abstractmethod
    def start(self, start_url: str, url_limit: int):
        """Used to start a crawler process."""


class ScreenshotCrawler(CrawlerProcess):
    def start(self, start_url: str, url_limit: int):
        package = ScreenshotPackage(start_url=start_url)
        start_crawl.delay(url=start_url, url_limit=url_limit, package_id=package.get_package_id())
        return package.get_package_id()
