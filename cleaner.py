import json
import re
import sys
import os
import html as html_module
import unicodedata
from datetime import datetime

try:
    from dateutil import parser as dateutil_parser  # optional, more robust
    _HAS_DATEUTIL = True
except Exception:
    _HAS_DATEUTIL = False

try:
    from bs4 import BeautifulSoup
    _HAS_BS4 = True
except Exception:
    _HAS_BS4 = False


def strip_html(text: str) -> str:
    if not text:
        return text
    if _HAS_BS4:
        # use bs4 when available for robust HTML stripping
        return BeautifulSoup(text, "lxml").get_text(" ", strip=True)
    # fallback simple regex to remove tags
    clean = re.sub(r"<[^>]+>", " ", text)
    return clean


def remove_control_chars(s: str) -> str:
    # remove C0 control characters except common whitespace (tab/newline)
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]+", "", s)


def collapse_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def clean_text(value: str) -> str:
    if value is None:
        return None
    if not isinstance(value, str):
        value = str(value)
    # unescape HTML entities
    value = html_module.unescape(value)
    # strip HTML tags
    value = strip_html(value)
    # normalize unicode
    value = unicodedata.normalize("NFKC", value)
    # remove invisible/control characters
    value = remove_control_chars(value)
    # collapse whitespace
    value = collapse_whitespace(value)
    return value


def clean_date(value: str) -> str:
    if value is None:
        return None
    value = clean_text(value)
    if not value:
        return None
    # Try dateutil if available (handles many formats)
    if _HAS_DATEUTIL:
        try:
            dt = dateutil_parser.parse(value)
            # return as ISO 8601 (UTC offset preserved if present)
            return dt.isoformat()
        except Exception:
            pass

    # Try direct ISO parsing
    try:
        # This will parse strings like '2026-02-02T00:00:00Z' or '2026-02-02'
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.isoformat()
    except Exception:
        pass

    # Common datetime formats to try
    patterns = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d %B %Y",
        "%B %d, %Y",
        "%d %b %Y",
    ]
    for p in patterns:
        try:
            dt = datetime.strptime(value, p)
            return dt.isoformat()
        except Exception:
            continue

    # As a last resort, extract an ISO-like substring (YYYY-MM-DD)
    m = re.search(r"(\d{4}-\d{2}-\d{2})", value)
    if m:
        try:
            dt = datetime.strptime(m.group(1), "%Y-%m-%d")
            return dt.isoformat()
        except Exception:
            pass

    # give up and return cleaned original
    return value


def clean_item(item):
    # recursively clean data structures
    if item is None:
        return None
    if isinstance(item, str):
        return clean_text(item)
    if isinstance(item, list):
        out = []
        for x in item:
            c = clean_item(x)
            if isinstance(c, str) and c == "":
                continue
            out.append(c)
        return out
    if isinstance(item, dict):
        out = {}
        for k, v in item.items():
            key_low = k.lower() if isinstance(k, str) else k
            if key_low in ("published", "published_at", "date", "date_published"):
                out[k] = clean_date(v)
            elif key_low in ("paragraphs", "body", "content") and isinstance(v, list):
                # clean each paragraph
                cleaned = [clean_text(p) for p in v if p is not None]
                cleaned = [c for c in cleaned if c]
                out[k] = cleaned
            else:
                out[k] = clean_item(v)
        return out
    # fallback for numbers/bools
    return item


def main():
    # Allow CLI args: input output
    in_file = sys.argv[1] if len(sys.argv) > 1 else "sample_data.json"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "cleaned_output.json"

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

    cleaned = clean_item(data)

    try:
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to write output '{out_file}': {e}")
        sys.exit(4)

    print(f"Wrote cleaned data to {out_file}")


if __name__ == "__main__":
    main()
