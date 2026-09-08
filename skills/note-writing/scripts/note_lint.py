#!/usr/bin/env python3
"""note_lint.py

note-writing向けの軽量lint。
文章の良し悪しを機械判定するのではなく、公開前に見直すべき箇所を指さす。
外部依存なし。

Usage:
    python3 skills/note-writing/scripts/note_lint.py article.md
    python3 skills/note-writing/scripts/note_lint.py article.md --max-chars 1499 --json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CONNECTIVE_COMMA = re.compile(
    r"^(でも|だから|そして|ただ|もちろん|たぶん|つまり|なんか|一方で|そのため|さらに)、"
)
SENTENCE_SPLIT = re.compile(r"(?<=[。！？!?])")
GENERIC_HEADINGS = {"背景", "概要", "まとめ", "結論", "はじめに", "おわりに"}
AI_ABSTRACT_WORDS = [
    "本質",
    "解像度",
    "熱量",
    "文脈",
    "営み",
    "構造的",
    "根本的",
    "革新的",
    "価値提供",
]
ANTITHESIS_PATTERNS = ["ではなく", "だけでなく"]


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :]
    return text


def extract_article_body(text: str) -> str:
    """標準出力なら「編集済み本文」だけを抽出。なければ全文を本文扱い。"""
    patterns = [
        r"(?ms)^# 編集済み本文\s*\n(.*?)(?=^# [^#]|\Z)",
        r"(?ms)^## 編集済み本文\s*\n(.*?)(?=^##? [^#]|\Z)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return m.group(1).strip()
    return strip_frontmatter(text).strip()


def visible_char_count(text: str) -> int:
    # ユーザー既定: 改行・空白・Markdown強調記号は数えない。
    cleaned = text
    cleaned = re.sub(r"```.*?```", "", cleaned, flags=re.S)
    cleaned = cleaned.replace("**", "").replace("__", "").replace("`", "")
    cleaned = re.sub(r"(?m)^#{1,6}\s*", "", cleaned)
    cleaned = re.sub(r"\s+", "", cleaned)
    return len(cleaned)


def plain_text(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = text.replace("**", "").replace("__", "")
    text = re.sub(r"(?m)^#{1,6}\s*", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    return text


def sentences(text: str) -> list[str]:
    out: list[str] = []
    for part in SENTENCE_SPLIT.split(plain_text(text)):
        s = part.strip()
        if s:
            out.append(s)
    return out


def paragraph_sentence_counts(text: str) -> list[int]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", plain_text(text)) if p.strip()]
    counts = []
    for p in paras:
        if p.startswith("#") or p.startswith("-"):
            continue
        counts.append(max(1, len([s for s in SENTENCE_SPLIT.split(p) if s.strip()])))
    return counts


def heading_names(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"(?m)^#{2,4}\s+(.+)$", text)]


def lint(text: str, max_chars: int) -> dict:
    body = extract_article_body(text)
    body_plain = plain_text(body)
    findings: list[dict] = []

    count = visible_char_count(body)
    if max_chars > 0 and count > max_chars:
        findings.append(
            {
                "severity": "P0",
                "type": "length",
                "message": f"本文が{count}字。上限{max_chars}字を{count-max_chars}字超過。",
            }
        )

    for idx, s in enumerate(sentences(body), start=1):
        compact = re.sub(r"\s+", "", s)
        commas = compact.count("、")
        n = len(compact)
        if n <= 40 and commas >= 2:
            findings.append(
                {
                    "severity": "P1",
                    "type": "comma_short_sentence",
                    "sentence": idx,
                    "message": f"短文({n}字)に読点{commas}個。語順変更か文分割を検討。",
                    "text": s,
                }
            )
        elif commas >= 3:
            findings.append(
                {
                    "severity": "P1",
                    "type": "comma_density",
                    "sentence": idx,
                    "message": f"一文に読点{commas}個。列挙でなければ再設計を検討。",
                    "text": s,
                }
            )

        if CONNECTIVE_COMMA.search(s.lstrip(" >-　")):
            findings.append(
                {
                    "severity": "P2",
                    "type": "connective_comma",
                    "sentence": idx,
                    "message": "短い文頭表現の直後に読点。なくても自然か確認。",
                    "text": s,
                }
            )

    for pattern in ANTITHESIS_PATTERNS:
        hits = body_plain.count(pattern)
        if hits >= 3:
            findings.append(
                {
                    "severity": "P1",
                    "type": "antithesis_repetition",
                    "message": f"「{pattern}」が{hits}回。対比構文の反復を確認。",
                }
            )

    abstract_hits = {w: body_plain.count(w) for w in AI_ABSTRACT_WORDS if body_plain.count(w)}
    total_abstract = sum(abstract_hits.values())
    if total_abstract >= 5 or len(abstract_hits) >= 4:
        findings.append(
            {
                "severity": "P2",
                "type": "abstract_word_cluster",
                "message": "抽象語がまとまって出ている。具体的な場面や普通の日本語に戻せないか確認。",
                "hits": abstract_hits,
            }
        )

    for heading in heading_names(body):
        normalized = re.sub(r"[*`_：:].*$", "", heading).strip()
        if normalized in GENERIC_HEADINGS:
            findings.append(
                {
                    "severity": "P2",
                    "type": "generic_heading",
                    "message": f"汎用見出し「{heading}」。内容を運ぶ見出しにできるか確認。",
                }
            )

    counts = paragraph_sentence_counts(body)
    if len(counts) >= 5:
        single_ratio = sum(1 for c in counts if c == 1) / len(counts)
        if single_ratio >= 0.8:
            findings.append(
                {
                    "severity": "P2",
                    "type": "one_sentence_paragraphs",
                    "message": f"1文段落が{single_ratio:.0%}。意図したリズムか確認。",
                }
            )

    return {
        "article_chars": count,
        "max_chars": max_chars,
        "p0": sum(1 for f in findings if f["severity"] == "P0"),
        "p1": sum(1 for f in findings if f["severity"] == "P1"),
        "p2": sum(1 for f in findings if f["severity"] == "P2"),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--max-chars", type=int, default=1499)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        text = args.file.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {exc}")
        return 1

    result = lint(text, args.max_chars)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"本文: {result['article_chars']}字 / 上限: {result['max_chars']}字")
        print(f"P0={result['p0']} P1={result['p1']} P2={result['p2']}")
        if not result["findings"]:
            print("findings: なし")
        for f in result["findings"]:
            print(f"[{f['severity']}] {f['type']}: {f['message']}")
            if f.get("text"):
                print(f"  {f['text']}")

    # lintは指さし。文章上のfindingではCIを止めない。
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
