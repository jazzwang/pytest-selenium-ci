import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

@pytest.fixture()
def setup(request):
    chrome_service = ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    chrome_options = webdriver.ChromeOptions()
    options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
    for option in options:
        chrome_options.add_argument(option)

    request.cls.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    yield request.cls.driver
    request.cls.driver.close()
