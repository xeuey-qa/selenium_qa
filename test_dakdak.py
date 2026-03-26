import pytest
import requests
import allure
import json
from page_dak import DakMainPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

# Создаем экземпляр Faker с русской локалью
fake = Faker('ru_RU')
@allure.feature("Интеграционные тесты (POM)")
def test_api_to_ui_pom(browser):
    with allure.step('Запрашиваем данные через API'):
        response = requests.get("https://jsonplaceholder.typicode.com/users/3")
        email_name = response.json()['email']
        allure.attach(json.dumps(response.json(), indent=4), 
                        name="API Response", attachment_type=allure.attachment_type.JSON)
    
    with allure.step('Создаем через факер должность'):
        random_job = fake.job() 

    main_page = DakMainPage(browser)
    with allure.step(f"Открываем дак дак сайт "):
        main_page.open()
        search_query = f"{email_name} {random_job}"
        main_page.search_for(search_query)

    with allure.step(f"Проверка поиска"):
        WebDriverWait(browser,10).until(EC.title_contains(email_name))
        assert email_name in browser.title

@allure.feature("API Testing")
@allure.story("Check status code")
def test_get_users_list():
    with allure.step("Отправляем запрос к API"):
        response = requests.get("https://reqres.in/api/users?page=2")
    
    with allure.step("Проверяем, что статус код 200"):
        assert response.status_code == 200
        
    with allure.step("Проверяем структуру данных"):
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        
        
        
    
            