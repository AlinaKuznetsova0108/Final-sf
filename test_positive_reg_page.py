from pages.Api_RegMail import RegEmail
from pages.auth import *
from selenium.webdriver.common.by import By
from pages.settings import valid_phone, valid_login, valid_password, \
    fake_firstname, fake_lastname, fake_password
import time
import pytest


class TestRegistration:
    
    # Выносим данные в тело класса для доступа к значениям переменных из всех функций класса:
    result_email, status_email = RegEmail().get_api_email()  # запрос на получение валидного почтового ящика
    email_reg = result_email[0]  # из запроса получаем валидный email

    @pytest.mark.reg
    @pytest.mark.positive
    def test_get_registration_valid(self, browser):

        # Разделяем email на имя и домен для использования в следующих запросах:
        sign_at = self.email_reg.find('@')
        mail_name = self.email_reg[0:sign_at]
        mail_domain = self.email_reg[sign_at + 1:len(self.email_reg)]
        assert self.status_email == 200, 'status_email error'
        assert len(self.result_email) > 0, 'len(result_email) > 0 -> error'

        # Нажимаем на кнопку Зарегистрироваться:
        page = AuthPage(browser)
        page.enter_reg_page()
        browser.implicitly_wait(2)
        assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

        page = RegPage(browser)
        page.enter_firstname(fake_firstname)
        browser.implicitly_wait(5)
        page.enter_lastname(fake_lastname)
        browser.implicitly_wait(5)
        page.enter_email(self.email_reg)
        browser.implicitly_wait(3)
        page.enter_password(fake_password)
        browser.implicitly_wait(3)
        page.enter_pass_conf(fake_password)
        browser.implicitly_wait(3)
        page.btn_click()
        time.sleep(30)  

        result_id, status_id = RegEmail().get_id_letter(mail_name, mail_domain)
        # Получаем id письма с кодом из почтового ящика:
        id_letter = result_id[0].get('id')
        # Сверяем полученные данные с нашими ожиданиями
        assert status_id == 200, "status_id error"
        assert id_letter > 0, "id_letter > 0 error"


        result_code, status_code = RegEmail().get_reg_code(mail_name, mail_domain, str(id_letter))

        # Получаем body из текста письма:
        text_body = result_code.get('body')
        # Извлекаем код из текста методом find:
        reg_code = text_body[text_body.find('Ваш код : ') + len('Ваш код : '):
                             text_body.find('Ваш код : ') + len('Ваш код : ') + 6]
       

        reg_digit = [int(char) for char in reg_code]
        browser.implicitly_wait(30)
        for i in range(0, 6):
            browser.find_elements(By.XPATH, '//input[@inputmode="numeric"]')[i].send_keys(reg_code[i])
            browser.implicitly_wait(5)
        browser.implicitly_wait(30)

        assert page.get_relative_link() == '/account_b2c/page', 'Регистрация НЕ пройдена'
        page.driver.save_screenshot('reg_done.png')
        
        page.driver.save_screenshot('reg_done.png')
        print(self.email_reg, fake_password)
        with open(r"../pages/Settings.py", 'r', encoding='utf8') as file:
            lines = []
            print(lines)
            for line in file.readlines():
                if 'valid_email' in line:
                    lines.append(f"valid_email = '{str(self.email_reg)}'\n")
                elif 'valid_pass_reg' in line:
                    lines.append(f"valid_pass_reg = '{fake_password}'\n")
                else:
                    lines.append(line)
        with open(r"../pages/Settings.py", 'w', encoding='utf8') as file:
            file.writelines(lines)
