import os
import json
import shutil
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

from parser.text_reader import extract_text
from parser.extractor import extract_basic_info
from parser.normalize import normalize_whitespace


def parse_args():
    parser = argparse.ArgumentParser(description="Парсер резюме с фильтрацией и аналитикой")
    parser.add_argument("--input", "-i", default="data/resumes", help="Папка с резюме (.pdf, .docx)")
    parser.add_argument("--output", "-o", default="data/output", help="Папка для результатов")
    parser.add_argument("--export-xlsx", action="store_true", help="Сохранить результат в Excel")
    parser.add_argument("--filter", "-f", nargs="+", help="Фильтрация по навыкам")
    parser.add_argument("--any", action="store_true", help="Совпадение по любому из навыков (по умолчанию — по всем)")
    parser.add_argument("--search", "-s", type=str, help="Поиск по ключевым словам")
    parser.add_argument("--stats", action="store_true", help="Показать статистику по навыкам")
    parser.add_argument("--copy-matching", action="store_true", help="Скопировать подходящие резюме в output/matched/")
    return parser.parse_args()


args = parse_args()
INPUT_DIR = args.input
OUTPUT_DIR = args.output
os.makedirs(OUTPUT_DIR, exist_ok=True)

results = []

# Обработка всех резюме
for filename in os.listdir(INPUT_DIR):
    filepath = os.path.join(INPUT_DIR, filename)
    try:
        text = extract_text(filepath)
        text = normalize_whitespace(text)
        info = extract_basic_info(text)
        info['filename'] = filename
        results.append(info)

        # Сохраняем извлечённый текст
        with open(os.path.join(OUTPUT_DIR, f"{os.path.splitext(filename)[0]}.txt"), "w", encoding="utf-8") as f:
            f.write(text)

        print(f"[+] Обработано: {filename}")
    except Exception as e:
        print(f"[!] Ошибка обработки {filename}: {e}")

# Фильтрация по навыкам
filtered_results = results
if args.filter:
    filter_skills = [s.lower() for s in args.filter]

    def matches_skills(candidate):
        candidate_skills = [s.lower() for s in candidate.get("skills", [])]
        return any(skill in candidate_skills for skill in filter_skills) if args.any \
            else all(skill in candidate_skills for skill in filter_skills)

    filtered_results = list(filter(matches_skills, filtered_results))
    mode = "любому" if args.any else "всем"
    print(f"[i] Найдено {len(filtered_results)} кандидатов по {mode} из навыков: {', '.join(args.filter)}")

# Поиск по ключевым словам
if args.search:
    keywords = [kw.lower() for kw in args.search.split()]

    def matches_search(candidate):
        fields = [
            candidate.get("name", ""),
            candidate.get("email", ""),
            candidate.get("phone", ""),
            " ".join(candidate.get("skills", [])),
            " ".join(candidate.get("experience", [])),
            " ".join(candidate.get("education", []))
        ]
        return all(kw in " ".join(fields).lower() for kw in keywords)

    filtered_results = list(filter(matches_search, filtered_results))
    print(f"[i] Найдено {len(filtered_results)} кандидатов по поиску: '{args.search}'")

# Статистика и визуализация
if args.stats:
    total = len(filtered_results)
    all_skills = [s.lower() for c in filtered_results for s in c.get("skills", [])]
    skill_counter = Counter(all_skills)
    avg_skills = round(len(all_skills) / total, 2) if total else 0

    print("\n📊 Статистика:")
    print(f"Всего резюме: {total}")
    print(f"Среднее количество навыков: {avg_skills}")
    print("Топ-10 навыков:")
    for skill, count in skill_counter.most_common(10):
        print(f"  {skill} — {count}")

    if skill_counter:
        skills, counts = zip(*skill_counter.most_common(10))
        plt.figure(figsize=(10, 6))
        plt.bar(skills, counts)
        plt.title("Топ-10 навыков среди кандидатов")
        plt.ylabel("Количество")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_path = os.path.join(OUTPUT_DIR, "skills_chart.png")
        plt.savefig(chart_path)
        print(f"[✓] График сохранён: {chart_path}")

# Копирование подходящих резюме
if args.copy_matching:
    matched_dir = os.path.join(OUTPUT_DIR, "matched")
    os.makedirs(matched_dir, exist_ok=True)

    for candidate in filtered_results:
        src = os.path.join(INPUT_DIR, candidate["filename"])
        dst = os.path.join(matched_dir, candidate["filename"])
        try:
            shutil.copy2(src, dst)
        except Exception as e:
            print(f"[!] Ошибка копирования {candidate['filename']}: {e}")

    print(f"[✓] Скопировано файлов: {len(filtered_results)} в {matched_dir}")

# Экспорт результатов
with open(os.path.join(OUTPUT_DIR, "summary.json"), "w", encoding="utf-8") as f:
    json.dump(filtered_results, f, indent=2, ensure_ascii=False)

if args.export_xlsx:
    pd.DataFrame(filtered_results).to_excel(os.path.join(OUTPUT_DIR, "summary.xlsx"), index=False)
    print("[✓] summary.xlsx сохранён.")