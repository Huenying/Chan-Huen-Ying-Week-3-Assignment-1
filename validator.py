import json
import os
import sys
from urllib.parse import urlparse


MIN_CONTENT_LENGTH = 100  # characters for combined content
MIN_SUMMARY_LENGTH = 50


def is_valid_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def extract_content(record: dict) -> str:
    # Content can be 'paragraphs' (list) or 'summary' or 'content'
    if not isinstance(record, dict):
        return ""
    if "paragraphs" in record and isinstance(record["paragraphs"], list):
        return "\n\n".join([p for p in record["paragraphs"] if isinstance(p, str)])
    if "content" in record and isinstance(record["content"], list):
        return "\n\n".join([p for p in record["content"] if isinstance(p, str)])
    if "summary" in record and isinstance(record["summary"], str):
        return record["summary"]
    if "body" in record and isinstance(record["body"], str):
        return record["body"]
    return ""


def validate_record(record: dict) -> dict:
    errors = []
    # Title
    title = record.get("title") if isinstance(record, dict) else None
    if not title or not isinstance(title, str) or not title.strip():
        errors.append("missing_or_empty_title")

    # URL
    url = record.get("url") if isinstance(record, dict) else None
    if not url:
        errors.append("missing_url")
    elif not is_valid_url(url):
        errors.append("invalid_url_format")

    # Content
    content = extract_content(record)
    if not content or not content.strip():
        errors.append("missing_content")
    else:
        if len(content) < MIN_CONTENT_LENGTH:
            # also check summary as secondary
            summary = record.get("summary")
            if summary and isinstance(summary, str) and len(summary) >= MIN_SUMMARY_LENGTH:
                pass
            else:
                errors.append(f"content_too_short_{len(content)}chars")

    valid = len(errors) == 0
    return {"valid": valid, "errors": errors, "title": title, "url": url, "content_length": len(content)}


def main():
    in_file = sys.argv[1] if len(sys.argv) > 1 else "cleaned_output.json"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "validation_report.json"

    if not os.path.isabs(in_file):
        in_file = os.path.join(os.getcwd(), in_file)
    if not os.path.exists(in_file):
        print(f"Input file not found: {in_file}")
        sys.exit(2)

    try:
        with open(in_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to read/parse JSON '{in_file}': {e}")
        sys.exit(3)

    records = []
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        records = [data]
    else:
        print("Unexpected JSON structure: must be object or array of objects")
        sys.exit(4)

    report = {"total": len(records), "valid_count": 0, "invalid_count": 0, "items": []}
    for idx, rec in enumerate(records):
        res = validate_record(rec)
        if res["valid"]:
            report["valid_count"] += 1
        else:
            report["invalid_count"] += 1
        item = {"index": idx, "valid": res["valid"], "errors": res["errors"], "title": res.get("title"), "url": res.get("url"), "content_length": res.get("content_length")}
        report["items"].append(item)

    try:
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to write report '{out_file}': {e}")
        sys.exit(5)

    # Print concise summary
    print(f"Validation complete — total: {report['total']}, valid: {report['valid_count']}, invalid: {report['invalid_count']}")
    if report['invalid_count'] > 0:
        print("Invalid items with reasons:")
        for it in report['items']:
            if not it['valid']:
                print(f" - index {it['index']}: {it['errors']}")


if __name__ == "__main__":
    main()
