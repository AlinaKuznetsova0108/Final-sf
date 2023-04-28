import os
from dotenv import load_dotenv
from faker import Faker
import string
load_dotenv()

fake_ru = Faker('ru_RU')
fake_firstname = fake_ru.first_name()
fake_lastname = fake_ru.last_name()
fake_phone = fake_ru.phone_number()
fake = Faker()
fake_password = fake.password()
fake_login = fake.user_name()
fake_email = fake.email()


valid_phone = os.getenv('phone')
valid_login = os.getenv('login')
valid_password = os.getenv('password')
invalid_ls = '352010007897'

valid_email = 'hht98jid@tyrvo.com'
valid_pass_reg = 'FLLbb341'


def generate_string_rus(n):
    return 'б' * n


def generate_string_en(n):
    return 'x' * n


def english_chars():
    return 'qwertyuiopasdfghjklzxcvbnm'


def russian_chars():
    return 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'


def special_chars():
    return f'{string.punctuation}'
