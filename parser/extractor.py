import re
from typing import Dict, List
from parser.skills_list import SKILLS


def extract_email(text: str) -> str:
    """
    Извлекает первый email-адрес из текста.
    Поддерживает стандартные email-форматы.
    """
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group() if match else ''


def extract_phone(text: str) -> str:
    """
    Извлекает первый номер телефона из текста.
    Поддерживает форматы +7 и 8 с пробелами/скобками.
    Удаляет неразрывные и тонкие пробелы перед поиском.
    """
    text = text.replace('\u00A0', ' ').replace('\u2009', ' ')
    match = re.search(r'(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}', text)
    return match.group() if match else ''


def extract_name(text: str) -> str:
    """
    Извлекает ФИО из первых строк текста.
    Использует шаблон: Три слова с заглавных букв (Фамилия Имя Отчество).
    """
    lines = text.strip().split('\n')
    for line in lines[:5]:
        if re.fullmatch(r'[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+(\s[А-ЯЁ][а-яё]+)?', line.strip()):
            return line.strip()
    return ''


def extract_skills(text: str) -> List[str]:
    """
    Ищет ключевые навыки из словаря SKILLS в тексте.
    Использует поиск по словам (через границы слов).
    """
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))


def extract_block(text: str, keywords: List[str], max_lines: int = 10) -> List[str]:
    """
    Извлекает до `max_lines` строк после обнаружения одного из ключевых слов.
    Используется для выделения блока опыта или образования.
    """
    lines = text.split('\n')
    block = []

    for i, line in enumerate(lines):
        lower_line = line.strip().lower()
        if any(kw in lower_line for kw in keywords):
            block = [lines[j].strip() for j in range(i + 1, min(i + 1 + max_lines, len(lines)))]
            break

    return [line for line in block if line]


def extract_experience(text: str) -> List[str]:
    """
    Извлекает блок "Опыт работы" из текста.
    """
    return extract_block(text, keywords=[
        "опыт работы", "трудовая деятельность", "стаж работы", "карьера"
    ])


def extract_education(text: str) -> List[str]:
    """
    Извлекает блок "Образование" из текста.
    """
    return extract_block(text, keywords=[
        "образование", "учёба", "вуз", "университет", "колледж"
    ])


def extract_basic_info(text: str) -> Dict[str, any]:
    """
    Объединённая функция: извлекает ФИО, почту, телефон, навыки, опыт и образование.
    Возвращает словарь с ключами: name, email, phone, skills, experience, education.
    """
    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skills(text),
        'experience': extract_experience(text),
        'education': extract_education(text),
    }