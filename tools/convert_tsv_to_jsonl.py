"""
크라우드소싱 제출물(유의어군 TSV + 상황 TSV)을 JSONL로 변환하는 도구

사용법:
  python convert_tsv_to_jsonl.py word_groups.tsv scenarios.tsv -o output.jsonl
"""

import csv
import json
import argparse
import sys


DOMAIN_CODE_MAP = {
    "감각 표현": "sensory",
    "감정 표현": "emotional",
    "판단 표현": "judgement",
    "감상 표현": "appreciation",
    "상징 표현": "symbolic",
}

CATEGORY_CODE_MAP = {
    "시각": "visual", "미각": "gustatory", "촉각": "tactile",
    "청각": "auditory", "후각": "olfactory",
    "긍정 감정": "positive", "부정 감정": "negative", "복합 감정": "complex",
    "사회적 관계": "social", "능력/성품 판단": "ability",
    "능력/성품": "ability", "상황 판단": "situation",
    "심미적 평가": "aesthetic", "가치 평가": "value",
    "의태어": "mimetic", "의성어": "onomatopoeia",
}


def load_word_groups(path: str) -> dict:
    groups = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            gid = row["유의어군번호"].strip()
            groups[gid] = {
                "domain": row["도메인"].strip(),
                "category": row["카테고리"].strip(),
                "subcategory": row["소분류"].strip(),
                "words": [
                    row["단어1"].strip(),
                    row["단어2"].strip(),
                    row["단어3"].strip(),
                    row["단어4"].strip(),
                ],
            }
    return groups


def load_scenarios(path: str) -> list[dict]:
    scenarios = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for i, row in enumerate(reader, start=2):
            scenarios.append({
                "line": i,
                "group_id": row["유의어군번호"].strip(),
                "scenario": row["상황"].strip(),
                "answer": row["정답"].strip(),
            })
    return scenarios


def convert(groups_path: str, scenarios_path: str, output_path: str):
    groups = load_word_groups(groups_path)
    scenarios = load_scenarios(scenarios_path)

    items = []
    errors = []
    id_counters = {}

    for s in scenarios:
        gid = s["group_id"]
        if gid not in groups:
            errors.append(f"상황 행 {s['line']}: 유의어군 번호 '{gid}'를 찾을 수 없음")
            continue

        group = groups[gid]
        scenario = s["scenario"]
        answer = s["answer"]

        # 검증
        if "___" not in scenario:
            errors.append(f"상황 행 {s['line']}: 빈칸(___)이 없음")
            continue

        # ID 생성
        domain_code = DOMAIN_CODE_MAP.get(group["domain"], group["domain"])
        cat_code = CATEGORY_CODE_MAP.get(group["category"], group["category"])
        counter_key = f"{domain_code}_{cat_code}"
        id_counters[counter_key] = id_counters.get(counter_key, 0) + 1
        item_id = f"{domain_code}_{cat_code}_{id_counters[counter_key]:03d}"

        items.append({
            "id": item_id,
            "domain": group["domain"],
            "category": group["category"],
            "subcategory": group["subcategory"],
            "word_group": group["words"],
            "scenario": scenario,
            "choices": group["words"],
            "answer": answer,
        })

    if errors:
        print(f"경고: {len(errors)}건의 오류", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)

    with open(output_path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"변환 완료: {len(items)}문항 -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="유의어군 TSV + 상황 TSV -> JSONL 변환")
    parser.add_argument("word_groups", help="유의어군 TSV 파일")
    parser.add_argument("scenarios", help="상황 문항 TSV 파일")
    parser.add_argument("-o", "--output", default="output.jsonl", help="출력 JSONL 파일")
    args = parser.parse_args()
    convert(args.word_groups, args.scenarios, args.output)


if __name__ == "__main__":
    main()
