#!/usr/bin/env python
import argparse
import json
import re
import shutil
from copy import deepcopy
from datetime import datetime
from pathlib import Path


DEFAULT_CATEGORY_ORDER = [
    "功能用例",
    "表单校验",
    "边界值",
    "异常场景",
    "界面交互",
    "权限安全",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a revised payload from requirement changes based on an existing payload."
    )
    parser.add_argument("--change-json", required=True, help="Path to UTF-8 change evidence JSON.")
    parser.add_argument(
        "--workspace",
        default=".",
        help="Workspace path used to locate the latest payload/workbook baseline.",
    )
    parser.add_argument("--base-json", help="Optional explicit baseline payload path.")
    parser.add_argument("--base-xlsx", help="Optional explicit baseline workbook path.")
    parser.add_argument("--output-dir", help="Optional output directory for the new payload copy.")
    return parser.parse_args()


def normalize_text(value):
    return str(value or "").strip()


def extract_terms(text):
    text = normalize_text(text)
    return [
        token.lower()
        for token in re.findall(r"[\u4e00-\u9fffA-Za-z0-9]+", text)
        if len(token) > 1
    ]


def extract_phrases(text):
    compact = re.sub(r"\s+", "", normalize_text(text))
    phrases = []
    for size in range(2, min(len(compact), 8)):
        for index in range(0, len(compact) - size + 1):
            snippet = compact[index : index + size].lower()
            if snippet not in phrases:
                phrases.append(snippet)
    return phrases


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, payload):
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def locate_latest_payload(workspace):
    candidates = sorted(
        Path(workspace).rglob("*payload*.json"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    for candidate in candidates:
        if candidate.name == "base_payload.json":
            continue
        return candidate
    return None


def locate_latest_workbook(workspace):
    candidates = sorted(
        Path(workspace).rglob("*.xlsx"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def split_filename_suffix(stem):
    match = re.match(r"^(.*?)(?:_(\d{2}))?$", stem)
    if match:
        return match.group(1), int(match.group(2)) if match.group(2) else None
    return stem, None


def next_versioned_path(base_path, output_dir=None):
    base_path = Path(base_path)
    target_dir = Path(output_dir) if output_dir else base_path.parent
    root_stem, current_suffix = split_filename_suffix(base_path.stem)
    start = (current_suffix + 1) if current_suffix is not None else 1

    for number in range(start, start + 1000):
        candidate = target_dir / f"{root_stem}_{number:02d}{base_path.suffix}"
        if not candidate.exists():
            return candidate
    raise RuntimeError("Unable to determine next versioned file name.")


def category_map(payload):
    return {category["name"]: category for category in payload.get("categories", [])}


def collect_case_text(case):
    meta = case.get("_meta", {})
    parts = [
        normalize_text(case.get("模块")),
        normalize_text(case.get("用例标题")),
        normalize_text(case.get("测试步骤")),
        normalize_text(case.get("预期结果")),
        normalize_text(case.get("备注")),
        normalize_text(meta.get("source_requirement")),
        " ".join(meta.get("keywords", [])),
    ]
    return " ".join(part for part in parts if part)


def score_case(case, terms, phrases):
    text = collect_case_text(case).lower()
    title = normalize_text(case.get("用例标题")).lower()
    source_requirement = normalize_text(case.get("_meta", {}).get("source_requirement")).lower()
    keywords = " ".join(case.get("_meta", {}).get("keywords", [])).lower()

    score = 0
    matched_terms = []
    for term in terms:
        if term in source_requirement:
            score += 4
            matched_terms.append(term)
        elif term in title:
            score += 3
            matched_terms.append(term)
        elif term in keywords:
            score += 2
            matched_terms.append(term)
        elif term in text:
            score += 1
            matched_terms.append(term)
    for phrase in phrases:
        if phrase in source_requirement:
            score += 2
            matched_terms.append(phrase)
        elif phrase in title:
            score += 1
            matched_terms.append(phrase)
    return score, sorted(set(matched_terms))


def find_impacted_cases(payload, change_content):
    terms = extract_terms(change_content)
    phrases = extract_phrases(change_content)
    matches = []
    for category in payload.get("categories", []):
        for case in category.get("cases", []):
            score, matched_terms = score_case(case, terms, phrases)
            if score <= 0:
                continue
            matches.append(
                {
                    "category": category["name"],
                    "case_id": normalize_text(case.get("用例编号")),
                    "title": normalize_text(case.get("用例标题")),
                    "score": score,
                    "matched_terms": matched_terms,
                }
            )
    matches.sort(key=lambda item: (-item["score"], item["case_id"]))
    return matches


def next_case_id(payload, category_name):
    prefix_map = {
        "功能用例": "FUNC",
        "表单校验": "VAL",
        "边界值": "BOUND",
        "异常场景": "ERR",
        "界面交互": "UI",
        "权限安全": "SEC",
    }
    prefix = prefix_map.get(category_name, "CASE")
    highest = 0
    for category in payload.get("categories", []):
        for case in category.get("cases", []):
            case_id = normalize_text(case.get("用例编号"))
            if prefix not in case_id:
                continue
            number_match = re.search(r"(\d+)$", case_id)
            if number_match:
                highest = max(highest, int(number_match.group(1)))
    return f"LW-{prefix}-{highest + 1:03d}"


def infer_best_category(change_content):
    content = normalize_text(change_content)
    if any(keyword in content for keyword in ["校验", "必填", "格式"]):
        return "表单校验"
    if any(keyword in content for keyword in ["最大", "最小", "长度", "范围"]):
        return "边界值"
    if any(keyword in content for keyword in ["页面", "展示", "按钮", "下拉", "交互"]):
        return "界面交互"
    if any(keyword in content for keyword in ["权限", "角色", "安全"]):
        return "权限安全"
    if any(keyword in content for keyword in ["异常", "失败", "报错"]):
        return "异常场景"
    return "功能用例"


def apply_modify(payload, matches, change_content):
    updated_case_ids = []
    top_score = matches[0]["score"] if matches else 0
    eligible_ids = {
        item["case_id"]
        for item in matches
        if item["score"] == top_score or item["score"] >= max(2, top_score - 1)
    }

    for category in payload.get("categories", []):
        for case in category.get("cases", []):
            if normalize_text(case.get("用例编号")) not in eligible_ids:
                continue
            case["备注"] = append_note(case.get("备注"), f"已根据变更更新: {change_content}")
            title = normalize_text(case.get("用例标题"))
            if "已更新" not in title:
                case["用例标题"] = f"{title}（已更新）"
            case["预期结果"] = append_note(case.get("预期结果"), f"变更参考: {change_content}")
            meta = case.setdefault("_meta", {})
            meta["source_requirement"] = append_note(meta.get("source_requirement"), change_content)
            meta["keywords"] = merge_keywords(meta.get("keywords", []), extract_terms(change_content))
            updated_case_ids.append(normalize_text(case.get("用例编号")))
    return updated_case_ids


def apply_add(payload, change_content):
    category_name = infer_best_category(change_content)
    categories = category_map(payload)
    target_category = categories[category_name]
    new_case_id = next_case_id(payload, category_name)
    new_case = {
        "用例编号": new_case_id,
        "模块": payload.get("module_name", ""),
        "用例标题": f"根据变更新增: {change_content[:24]}",
        "前置条件": "基于现有业务前置条件执行",
        "测试步骤": f"按变更要求验证: {change_content}",
        "预期结果": "系统表现满足最新需求变更",
        "优先级": "中",
        "类型": category_name,
        "备注": "由需求变更新增",
        "_meta": {
            "source_requirement": change_content,
            "keywords": extract_terms(change_content),
        },
    }
    target_category["cases"].append(new_case)
    return [new_case_id]


def apply_delete(payload, matches, change_content):
    removed_case_ids = []
    target_ids = {item["case_id"] for item in matches if item["score"] >= 3}
    for category in payload.get("categories", []):
        kept_cases = []
        for case in category.get("cases", []):
            case_id = normalize_text(case.get("用例编号"))
            if case_id in target_ids:
                removed_case_ids.append(case_id)
                continue
            kept_cases.append(case)
        category["cases"] = kept_cases

    if not removed_case_ids:
        payload.setdefault("uncertainties", []).append(f"未找到可删除用例: {change_content}")
    return removed_case_ids


def append_note(existing, extra):
    existing_text = normalize_text(existing)
    if not existing_text:
        return extra
    if extra in existing_text:
        return existing_text
    return f"{existing_text} | {extra}"


def merge_keywords(existing, new_terms):
    merged = [normalize_text(item) for item in existing if normalize_text(item)]
    for term in new_terms:
        if term not in merged:
            merged.append(term)
    return merged


def reorder_categories(payload):
    categories = category_map(payload)
    ordered = []
    for name in DEFAULT_CATEGORY_ORDER:
        if name in categories:
            ordered.append(categories[name])
    for category in payload.get("categories", []):
        if category["name"] not in DEFAULT_CATEGORY_ORDER:
            ordered.append(category)
    payload["categories"] = ordered


def summarize(change_type, matches, updated_case_ids, added_case_ids, removed_case_ids):
    return {
        "change_type": change_type,
        "matched_cases": matches,
        "updated_cases": updated_case_ids,
        "added_cases": added_case_ids,
        "removed_cases": removed_case_ids,
    }


def main():
    args = parse_args()
    workspace = Path(args.workspace)
    change_payload = load_json(args.change_json)

    base_json = Path(args.base_json) if args.base_json else locate_latest_payload(workspace)
    if not base_json:
        raise FileNotFoundError("No baseline payload JSON was found in the workspace.")

    base_xlsx = Path(args.base_xlsx) if args.base_xlsx else locate_latest_workbook(workspace)
    if not base_xlsx:
        raise FileNotFoundError("No baseline workbook was found in the workspace.")

    payload = load_json(base_json)
    new_payload = deepcopy(payload)
    new_payload["schema_version"] = "v2.1"
    new_payload["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_payload["revision"] = int(new_payload.get("revision", 0)) + 1
    new_payload["based_on"] = base_xlsx.name
    new_payload["source_name"] = change_payload.get("source_name", new_payload.get("source_name", ""))
    if change_payload.get("module_name"):
        new_payload["module_name"] = change_payload["module_name"]

    change_type = change_payload["change_type"]
    change_content = change_payload["change_content"]
    matches = find_impacted_cases(new_payload, change_content)

    updated_case_ids = []
    added_case_ids = []
    removed_case_ids = []
    if change_type == "modify":
        updated_case_ids = apply_modify(new_payload, matches, change_content)
    elif change_type == "add":
        added_case_ids = apply_add(new_payload, change_content)
    elif change_type == "delete":
        removed_case_ids = apply_delete(new_payload, matches, change_content)
    else:
        raise ValueError("change_type must be one of: add, modify, delete")

    if not updated_case_ids and not added_case_ids and not removed_case_ids:
        new_payload.setdefault("uncertainties", []).append(f"未自动命中明确变更: {change_content}")

    reorder_categories(new_payload)

    output_dir = Path(args.output_dir) if args.output_dir else base_json.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    new_payload_path = next_versioned_path(base_json, output_dir=output_dir)
    write_json(new_payload_path, new_payload)

    summary = summarize(change_type, matches, updated_case_ids, added_case_ids, removed_case_ids)
    print(
        json.dumps(
            {
                "base_payload": str(base_json.resolve()),
                "base_workbook": str(base_xlsx.resolve()),
                "new_payload": str(new_payload_path.resolve()),
                "revision": new_payload["revision"],
                **summary,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
