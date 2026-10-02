#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
llm_checker.py - Vérification manuelle des LLM (bouton UI)
"""
import requests

def check_all():
    results = {}
    # Ollama
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=3)
        if r.status_code == 200:
            data = r.json()
            models = [m["name"] for m in data.get("models", [])]
            results["ollama"] = {"ok": True, "models": models}
        else:
            results["ollama"] = {"ok": False, "error": f"HTTP {r.status_code}"}
    except Exception as e:
        results["ollama"] = {"ok": False, "error": str(e)}

    # Torch
    try:
        import torch
        results["torch"] = {"ok": True, "version": torch.__version__, "cuda": torch.cuda.is_available()}
    except ImportError:
        results["torch"] = {"ok": False, "error": "non installé"}

    return results

if __name__ == "__main__":
    import json
    print(json.dumps(check_all(), indent=2, ensure_ascii=False))
