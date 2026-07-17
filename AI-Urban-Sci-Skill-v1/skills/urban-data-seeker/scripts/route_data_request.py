#!/usr/bin/env python3
"""Rank bundled urban data source/platform skills for a user request."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
from urllib.parse import urlparse


ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "references" / "route_index.compact.jsonl"


def load_index(path: pathlib.Path = INDEX) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def host_of(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url if "://" in url else f"https://{url}")
    return parsed.netloc.lower() or parsed.path.lower().split("/")[0]


def contains_phrase(haystack: str, phrase: str) -> bool:
    phrase = normalize(phrase)
    if not phrase:
        return False
    if re.search(r"[$/.:-]", phrase):
        return phrase in haystack
    return re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", haystack) is not None


def score_entry(entry: dict, query: str, url: str, direct_download: bool) -> tuple[int, list[str], str]:
    text = normalize(" ".join([query, url]))
    host = host_of(url)
    score = 0
    reasons: list[str] = []
    route_type = "discovery"

    alias_hits = [a for a in entry.get("aliases", []) if contains_phrase(text, a)]
    if alias_hits:
        score += 120 + min(30, 5 * len(alias_hits))
        reasons.append(f"alias={alias_hits[:3]}")
        route_type = "exact_source" if entry.get("role") == "source" else "platform_fingerprint"

    domain_hits = []
    for domain in entry.get("domains", []):
        d = normalize(domain)
        if d and (d in host or d in text):
            domain_hits.append(domain)
    if domain_hits:
        score += 110 + min(30, 5 * len(domain_hits))
        reasons.append(f"domain={domain_hits[:3]}")
        route_type = "url_domain"

    fp_hits = [f for f in entry.get("platform_fingerprints", []) if contains_phrase(text, str(f))]
    if fp_hits:
        score += 90 + min(25, 5 * len(fp_hits))
        reasons.append(f"fingerprint={fp_hits[:3]}")
        if route_type == "discovery":
            route_type = "platform_fingerprint"

    topic_hits = [t for t in entry.get("topics", []) if contains_phrase(text, t)]
    if topic_hits:
        score += 45 + min(45, 5 * len(topic_hits))
        reasons.append(f"topic={topic_hits[:4]}")
        if route_type == "discovery":
            route_type = "source_topic"

    action_hits = [a for a in entry.get("actions", []) if contains_phrase(text, str(a))]
    if action_hits:
        score += 15
        reasons.append(f"action={action_hits[:3]}")

    role = entry.get("role")
    broad_terms = ["find", "discover", "source", "dataset", "where can i get", "portal", "catalog"]
    if role == "platform" and any(term in text for term in broad_terms):
        score += 15
    if role == "source" and alias_hits:
        score += 60

    if direct_download and entry.get("auth_required"):
        score -= 40
        reasons.append("direct_download_auth_penalty")

    return score, reasons, route_type


def route(query: str, url: str = "", top_k: int = 5, direct_download: bool = False) -> dict:
    ranked = []
    for entry in load_index():
        score, reasons, route_type = score_entry(entry, query, url, direct_download)
        if score >= 60:
            ranked.append((score, entry["rank"], route_type, reasons, entry))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    selected_items = ranked[:top_k]
    selected = []
    for score, _, route_type, reasons, entry in selected_items:
        confidence = "high" if score >= 110 else "medium" if score >= 60 else "low"
        selected.append({
            "skill": entry["name"],
            "role": entry["role"],
            "score": score,
            "confidence": confidence,
            "route_type": route_type,
            "why": reasons or ["fallback"],
            "skill_path": entry["skill_path"],
            "skill_root": entry["skill_root"],
            "tool_entrypoints": entry.get("tool_entrypoints", []),
            "external_candidate_count": entry.get("external_candidate_count", 0),
        })
    return {
        "schema": "urban_data_seeker.route.v1",
        "query": query,
        "url": url,
        "selected": selected,
        "next_step": "Open only selected source/platform skill_path files, then run find/probe before fetch.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--url", default="")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--direct-download", action="store_true")
    args = parser.parse_args()
    print(json.dumps(route(args.query, args.url, args.top_k, args.direct_download), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
