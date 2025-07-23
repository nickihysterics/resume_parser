# Resume Parser and Analyzer

Утилита на Python для автоматической обработки резюме (.pdf и .docx), извлечения ключевой информации, фильтрации по навыкам и генерации аналитических отчётов.

## Возможности

- Поддержка форматов `.pdf` и `.docx`
- Извлечение:
  - Фамилия Имя Отчество
  - Email
  - Телефон
  - Навыки (по заданному списку)
  - Опыт работы и образование
- Фильтрация по навыкам:
  - По всем указанным навыкам (`--filter`)
  - По любому из навыков (`--any`)
- Поиск по ключевым словам в тексте резюме (`--search`)
- Генерация статистики:
  - Подсчёт количества навыков
  - Гистограмма 10 самых популярных навыков
- Копирование подходящих резюме в отдельную папку (`--copy-matching`)
- Экспорт результатов в `.json` и `.xlsx`
- Юнит-тесты с использованием `pytest`

## Установка

```bash
git clone https://github.com/nickihysterics/resume-parser.git
cd resume-parser
pip install -r requirements.txt
```

> Убедитесь, что установлен Python 3.8 или выше.

## Структура проекта

```text
resume_parser/
├── data/
│   ├── resumes/           # Входные резюме (.pdf, .docx)
│   └── output/            # Результаты обработки
├── parser/
│   ├── extractor.py       # Извлечение информации
│   ├── normalize.py       # Очистка пробелов
│   ├── skills_list.py     # Список навыков
│   └── text_reader.py     # Чтение PDF и DOCX
├── tests/
│   ├── test_extractor.py
│   └── test_skills.py
├── main.py                # Основной интерфейс командной строки
└── README.md
```

## Использование

```bash
python main.py [опции]
```

### Аргументы

| Аргумент         | Описание |
|------------------|----------|
| `--input, -i`     | Путь к папке с резюме (по умолчанию: `data/resumes`) |
| `--output, -o`    | Папка для сохранения результатов (по умолчанию: `data/output`) |
| `--filter, -f`    | Список навыков для фильтрации (например: `--filter python django`) |
| `--any`           | Фильтрация по любому навыку (по умолчанию — по всем) |
| `--search, -s`    | Поиск по ключевым словам (например: `--search "python университет"`) |
| `--stats`         | Показ статистики и сохранение графика |
| `--export-xlsx`   | Экспорт результатов в Excel (`summary.xlsx`) |
| `--copy-matching` | Копирование подходящих резюме в `output/matched/` |

## Примеры использования

```bash
python main.py --filter python django
python main.py --filter python flask --any
python main.py --search "вуз python"
python main.py --stats
python main.py --export-xlsx
python main.py --copy-matching
```

## Тестирование

```bash
pytest
```

## Автор

Никита Мусин  
Telegram: [@nicki_hysterics](https://t.me/nicki_hysterics)  
GitHub: [github.com/nickihysterics](https://github.com/nickihysterics)

## Лицензия

Проект распространяется под лицензией MIT.
