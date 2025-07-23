import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from parser.extractor import extract_email, extract_phone, extract_name


def test_email_extraction():
    text = "Контакты: Иванов И.И. ivanov@example.com"
    assert extract_email(text) == "ivanov@example.com"

def test_phone_extraction():
    text = "Тел: +7 (999) 123-45-67"
    assert extract_phone(text) == "+7 (999) 123-45-67"

def test_name_extraction():
    text = "Иванов Иван Иванович\nРазработчик Python"
    assert extract_name(text) == "Иванов Иван Иванович"

@pytest.mark.parametrize("text,expected", [
    ("Почта: ivanov@example.com", "ivanov@example.com"),
    ("Email: user.name123@domain.co.uk", "user.name123@domain.co.uk"),
    ("Контакт: нет почты", ""),
    ("", "")
])
def test_extract_email(text, expected):
    assert extract_email(text) == expected


@pytest.mark.parametrize("text,expected", [
    ("Телефон: +7 (999) 123-45-67", "+7 (999) 123-45-67"),
    ("Тел: 8 912 456 78 90", "8 912 456 78 90"),
    ("Контакты: нет телефона", ""),
    ("", "")
])
def test_extract_phone(text, expected):
    assert extract_phone(text) == expected


@pytest.mark.parametrize("text,expected", [
    ("Иванов Иван Иванович\nPython-разработчик", "Иванов Иван Иванович"),
    ("Сидоров П.П.\nИнженер", ""),
    ("", "")
])
def test_extract_name(text, expected):
    assert extract_name(text) == expected