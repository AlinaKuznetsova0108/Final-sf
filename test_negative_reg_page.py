from pages.Api_RegMail import RegEmail
from pages.auth import *
from selenium.webdriver.common.by import By
from pages.settings import *
import time
import pytest


@pytest.mark.reg
@pytest.mark.negatvie
@pytest.mark.parametrize('firstname', ['', generate_string_rus(1), generate_string_rus(31),
                                       generate_string_rus(256), english_chars(), chinese_chars(),
                                       special_chars(), 11111],
                         ids=['empty', 'one char', '31 chars', '256 chars', 'english', 'chinese',
                              'special', 'number'])
def test_get_registration_invalid_format_firstname(browser, firstname):

    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(2)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(firstname)
    browser.implicitly_wait(5)
    page.enter_lastname(fake_lastname)
    browser.implicitly_wait(5)
    page.enter_email(fake_email)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(fake_password)
    browser.implicitly_wait(3)
    page.btn_click()

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)

    assert error_mess.text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'


@pytest.mark.reg
@pytest.mark.negatvie
@pytest.mark.parametrize('lastname', ['', generate_string_rus(1), generate_string_rus(31),
                                      generate_string_rus(256), english_chars(), chinese_chars(),
                                      special_chars(), 11111],
                         ids=['empty', 'one char', '31 chars', '256 chars', 'english', 'chinese',
                              'special', 'number'])
def test_get_registration_invalid_format_lastname(browser, lastname):

    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(2)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(fake_firstname)
    browser.implicitly_wait(5)
    page.enter_lastname(lastname)
    browser.implicitly_wait(5)
    page.enter_email(fake_email)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(fake_password)
    browser.implicitly_wait(3)
    page.btn_click()

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'


@pytest.mark.reg
@pytest.mark.negatvie
@pytest.mark.parametrize('phone', ['', 1, 7111111111, generate_string_rus(11), special_chars()],
                         ids=['empty', 'one digit', 'no 1 digit', 'string', 'specials'])
def test_get_registration_invalid_format_phone(browser, phone):
   
    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(2)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(fake_firstname)
    browser.implicitly_wait(5)
    page.enter_lastname(fake_lastname)
    browser.implicitly_wait(5)
    page.enter_email(phone)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(fake_password)
    browser.implicitly_wait(3)
    page.btn_click()

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, ' \
                              'или email в формате example@email.ru'


@pytest.mark.reg
@pytest.mark.negatvie
@pytest.mark.parametrize('email', ['', '@', '@.', '.', generate_string_rus(20), f'{russian_chars()}@mail.ru',
                                   f'{chinese_chars()}@mail.ru', 11111],
                         ids=['empty', 'at', 'at point', 'point', 'string', 'russian',
                              'chinese', 'numbers'])
def test_get_registration_invalid_format_email(browser, email):
    
    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(2)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(fake_firstname)
    browser.implicitly_wait(5)
    page.enter_lastname(fake_lastname)
    browser.implicitly_wait(5)
    page.enter_email(email)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(fake_password)
    browser.implicitly_wait(3)
    page.btn_click()

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, ' \
                              'или email в формате example@email.ru'


@pytest.mark.reg
@pytest.mark.negatvie
@pytest.mark.parametrize('address', [valid_phone, valid_email],
                         ids=['living phone', 'living email'])
def test_get_registration_living_account(browser, address):
    
    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(2)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(fake_firstname)
    browser.implicitly_wait(5)
    page.enter_lastname(fake_lastname)
    browser.implicitly_wait(5)
    page.enter_email(address)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(fake_password)
    browser.implicitly_wait(3)
    page.btn_click()

    card_modal_title = browser.find_element(*RegLocators.REG_CARD_MODAL)

    assert card_modal_title.text == 'Учётная запись уже существует'


@pytest.mark.reg
@pytest.mark.negatvie
def test_get_registration_diff_pass_and_pass_conf(browser):
 
    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(2)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

    page = RegPage(browser)
    page.enter_firstname(fake_firstname)
    browser.implicitly_wait(5)
    page.enter_lastname(fake_lastname)
    browser.implicitly_wait(5)
    page.enter_email(fake_email)
    browser.implicitly_wait(3)
    page.enter_password(fake_password)
    browser.implicitly_wait(3)
    page.enter_pass_conf(valid_pass_reg)
    browser.implicitly_wait(3)
    page.btn_click()

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Пароли не совпадают'
