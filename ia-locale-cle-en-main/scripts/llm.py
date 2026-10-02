#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
llm.py - Dialogue avec Ollama
"""
import requests
from typing import List, Dict, Optional

OLLAMA_HOST = "http://127.0.0.1:11434"

def list_models(host: str = OLLAMA_HOST) -> List[str]:
    try:
        r = requests.get(f"{host}/api/tags", timeout=5)
        data = r.json()
        return [m.get("name", "") for m in data.get("models", [])]
    except Exception:
        return []

def chat(message: str, model: str = "llama3.2", history: List[Dict] = None, system: str = "", temperature: float = 0.7, host: str = OLLAMA_HOST) -> str:
    """Chat simple avec Ollama."""
    if history is None:
        history = []
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    try:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature}
        }
        r = requests.post(f"{host}/api/chat", json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data.get("message", {}).get("content", "") or data.get("response", "")
    except Exception as e:
        return f"[Erreur LLM {model}: {e}] - Vérifiez que Ollama est démarré (ollama serve) et que le modèle est installé (ollama pull {model})"

def chat_stream(message: str, model: str = "llama3.2", history: List[Dict] = None, system: str = ""):
    """Générateur streaming."""
    if history is None:
        history = []
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    try:
        import json
        payload = {"model": model, "messages": messages, "stream": True}
        with requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, stream=True, timeout=120) as r:
            r.raise_for_status()
            full = ""
            for line in r.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line.decode())
                    chunk = data.get("message", {}).get("content", "")
                    if chunk:
                        full += chunk
                        yield full
                    if data.get("done"):
                        break
                except:
                    continue
    except Exception as e:
        yield f"[Erreur stream: {e}]"

def check_ollama(host: str = OLLAMA_HOST) -> bool:
    try:
        r = requests.get(f"{host}/api/tags", timeout=3)
        return r.status_code == 200
    except:
        return False
