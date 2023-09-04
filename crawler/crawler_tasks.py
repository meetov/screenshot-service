import celery
import selenium.webdriver.common.by
from selenium import webdriver

from crawler.config import CELERY_BROKER, CELERY_BACKEND
from crawler.package import ScreenshotPackage

app = celery.Celery(__name__,
                    broker=CELERY_BROKER,
                    backend=CELERY_BACKEND)


def get_driver():
    # experimented with Chrome, Firefox and remote selenium browser, but did not get
    # the configuration properly for the remote hub. i believe in production it is better to use
    # a remote instance of a driver/browser
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    return driver


def parse_urls(driver, url_limit):
    elements = driver.find_elements(selenium.webdriver.common.by.By.XPATH, '//body//*/a')
    follow_urls = set()
    for element in elements:
        follow_urls.add(element.get_attribute('href'))
        if len(follow_urls) >= (url_limit - 1):
            break
    return follow_urls


@app.task
def take_screenshot(url: str, package_id: int):
    package = ScreenshotPackage.from_id(package_id)
    driver = get_driver()
    driver.get(url)
    package.add_file(
        blob=driver.get_screenshot_as_png(),
        source_url=url
    )
    driver.quit()


@app.task
def start_crawl(url: str, url_limit: int, package_id: int):
    driver = get_driver()
    driver.get(url)
    follow_urls = parse_urls(driver, url_limit)
    # ensure the start page is also screenshot
    follow_urls.add(url)

    for follow_url in follow_urls:
        take_screenshot.delay(url=follow_url, package_id=package_id)
    driver.quit()
