import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pytest
import pytest
import allure
@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Проверяем, запущены ли мы в Docker (путь к драйверу будет существовать)
    docker_driver_path = "/usr/bin/chromedriver"
    
    if os.path.exists(docker_driver_path):
        service = Service(executable_path=docker_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        # Если мы локально на Маке — запускаем Safari
        driver = webdriver.Safari()
        driver.maximize_window()
    
    yield driver
    driver.quit()

# Магия: делаем скриншот, если тест упал
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        mode = "a" if "driver" in item.fixturenames else None
        if mode:
            driver = item.funcargs["driver"]
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )