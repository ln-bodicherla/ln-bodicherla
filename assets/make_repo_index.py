"""Rebuild the grouped "All projects" section of README.md from live GitHub data.

Run from the repo root: python3 assets/make_repo_index.py
Repos not listed in GROUPS are reported so they can be placed.
"""

import json
import re
import subprocess
from pathlib import Path

USER = "ln-bodicherla"

GROUPS = [
    ("AI agents & LLM tools", [
        "skillgate", "vibectl", "fluxly-agentic", "prism-fxly", "potluck", "super-memory-mcp",
        "MediMemory", "unifiedAI", "crewai-multi-agent", "langgraph-multi-agent",
        "rag-document-qa", "graphrag-knowledge-qa",
    ]),
    ("Machine learning: fraud, risk & anomaly detection", [
        "fraud-detection-ensemble", "gnn-fraud-rings", "node2vec-fraud-detection",
        "anomaly-detection-system", "vae-anomaly-detection", "credit-risk-scoring",
        "model-explainability-toolkit",
    ]),
    ("Machine learning: time series", ["lstm-predictive-maintenance", "temporal-fusion-transformer"]),
    ("Machine learning: LLMs, NLP & documents", [
        "llm-finetuning-qlora", "deepspeed-llm-finetuning", "nlp-ner-transformers",
        "spacy-custom-ner", "document-ai-extraction",
    ]),
    ("Machine learning: computer vision & generative models", [
        "clip-visual-search", "blip2-image-captioning", "yolov8-object-detection",
        "detectron2-instance-segmentation", "segment-anything-api", "stable-diffusion-controlnet",
        "instructpix2pix-editor",
    ]),
    ("Machine learning: serving & MLOps", [
        "onnx-model-optimization", "bentoml-model-serving", "mlops-model-serving",
        "fastapi-ml-microservice", "spring-boot-ml-api",
    ]),
    ("Learning resources", ["mlmap", "MachineLearning"]),
    ("Linux desktop", ["lumen-grid", "gnome-nautilus"]),
    ("macOS & iOS apps", [
        "sonic-land", "recall-mac", "claude-code-gui", "WireAudio", "action-prompter", "fxly-wall",
        "zune-project", "BoringCalendar", "BoringNotes", "BoringRadio", "BoringWeather",
    ]),
    ("Android apps", ["cubes-launcher", "fluxlyapp-android", "BoringWeatherAndroid"]),
    ("Web apps", [
        "fluxlyapp-ui", "avancio-central", "fxly", "gym-tuner", "gym-tuner-backend",
        "subbed-tube-search-view", "AtlasFlow", "project-people", "socialok", "WhatSlack",
        "newsblock_ui", "newsblock_api",
    ]),
    ("Data engineering", [
        "pipelineforge-fxly", "airflow-etl-pipeline", "prefect-data-pipeline", "feast-feature-store",
        "streaming-fraud-detection", "newsblock_etl",
    ]),
    ("Other", ["usm-demo", "Intra-Network-System-for-Communication---Java"]),
]

START, END = "<!-- repo-index:start -->", "<!-- repo-index:end -->"


def live_repos():
    out = subprocess.run(
        ["gh", "api", f"users/{USER}/repos", "--paginate", "-q",
         '.[]|select(.fork==false)|{name,description,archived,private}'],
        capture_output=True, text=True, check=True,
    ).stdout
    return {r["name"]: r for r in (json.loads(l) for l in out.splitlines() if l.strip())}


def cell(text):
    return (text or "").replace("|", "\\|").strip()


def build(repos):
    parts = [START, "", "### All projects", ""]
    placed = set()
    for title, names in GROUPS:
        rows = [repos[n] for n in names if n in repos and not repos[n]["archived"]]
        placed.update(names)
        if not rows:
            continue
        parts.append(f"<details>\n<summary><b>{title}</b> ({len(rows)})</summary>\n")
        parts.append("| Repo | Description |\n|---|---|")
        for r in rows:
            parts.append(f'| [{r["name"]}](https://github.com/{USER}/{r["name"]}) | {cell(r["description"])} |')
        parts.append("\n</details>\n")
    parts.append(END)
    missing = sorted(n for n, r in repos.items() if n not in placed and not r["archived"] and n != USER)
    return "\n".join(parts), missing


def main():
    readme = Path("README.md")
    text = readme.read_text()
    section, missing = build(live_repos())
    if START in text:
        text = re.sub(re.escape(START) + ".*?" + re.escape(END), section, text, flags=re.S)
    else:
        text = text.replace("### Open-source contributions", section + "\n\n### Open-source contributions", 1)
    readme.write_text(text)
    if missing:
        print("Not grouped yet:", ", ".join(missing))


if __name__ == "__main__":
    main()
