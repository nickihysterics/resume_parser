import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from parser.extractor import extract_skills
from parser.skills_list import SKILLS


@pytest.mark.parametrize("text,expected", [
    (
        "Знаю Python, работал с Django и Flask, немного с JavaScript.",
        ["python", "django", "flask", "javascript"]
    ),
    (
        "Умею пользоваться Excel и Word. Есть опыт в 1C.",
        ["excel", "word", "1c"]
    ),
    (
        "Базовые знания HTML, CSS и React.",
        ["html", "css", "react"]
    ),
    (
        "Работал с Docker, Kubernetes и GitLab. Немного в Linux.",
        ["docker", "kubernetes", "gitlab", "linux"]
    ),
    (
        "В резюме не указано ничего из списка навыков.",
        []
    ),
    (
        "",
        []
    ),
])
def test_extract_skills(text, expected):
    result = extract_skills(text)
    assert set(result) == set(expected)
    for skill in result:
        assert skill.lower() in SKILLS
