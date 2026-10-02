#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_model_manager.py - Gestion installation modèles (V2 clé en main)
"""
from enum import Enum
from pathlib import Path
import subprocess
import sys

class ModelCategory(str, Enum):
    LLM = "llm"
    STT = "stt"
    TTS = "tts"
    IMAGE = "image"
    EMBEDDING = "embedding"
    THREED = "3d"

MODELS_CATALOG = {
    ModelCategory.LLM: [
        {"name": "llama3.2", "size": "2GB", "desc": "Léger, rapide, défaut"},
        {"name": "mistral", "size": "4GB", "desc": "Bon équilibre"},
        {"name": "phi3", "size": "2GB", "desc": "Très léger"},
        {"name": "llava", "size": "4.7GB", "desc": "Vision"},
        {"name": "nous-hermes2", "size": "4GB", "desc": "Non censuré 🌙"},
        {"name": "openhermes", "size": "4GB", "desc": "Non censuré alt"},
    ],
    ModelCategory.STT: [
        {"name": "base", "size": "150MB", "desc": "Whisper base FR"},
        {"name": "small", "size": "500MB", "desc": "Whisper small FR"},
        {"name": "medium", "size": "1.5GB", "desc": "Whisper medium FR"},
    ],
    ModelCategory.TTS: [
        {"name": "fr_FR-siwis-medium", "size": "60MB", "desc": "Piper FR Siwis"},
        {"name": "fr_FR-upmc-medium", "size": "60MB", "desc": "Piper FR UPMC"},
    ],
    ModelCategory.IMAGE: [
        {"name": "stabilityai/stable-diffusion-2-1-base", "size": "5GB", "desc": "SD 2.1"},
    ],
    ModelCategory.EMBEDDING: [
        {"name": "sentence-transformers/all-MiniLM-L6-v2", "size": "90MB", "desc": "Embeddings RAG"},
    ],
    ModelCategory.THREED: [
        {"name": "trimesh+scikit-image", "size": "50MB", "desc": "Mailles + export STL/3MF"},
    ]
}

def list_models():
    for cat, models in MODELS_CATALOG.items():
        print(f"\n[{cat.value.upper()}]")
        for m in models:
            print(f"  - {m['name']} ({m['size']}) : {m['desc']}")

def install_ollama_model(name: str):
    print(f"  Pull {name}...")
    r = subprocess.run(["ollama", "pull", name])
    return r.returncode == 0

def install_by_category(category: str):
    try:
        cat = ModelCategory(category)
    except:
        print(f"Catégorie inconnue : {category}")
        return

    if cat == ModelCategory.LLM:
        for m in MODELS_CATALOG[cat]:
            install_ollama_model(m["name"])
    elif cat == ModelCategory.STT:
        try:
            from faster_whisper import WhisperModel
            for m in MODELS_CATALOG[cat]:
                print(f"  Téléchargement STT {m['name']}")
                WhisperModel(m["name"], device="cpu", compute_type="int8")
        except ImportError:
            print("faster-whisper non installé")
    else:
        print(f"Installation {cat.value} : à implémenter / téléchargement à la demande")

def install_all():
    for cat in ModelCategory:
        install_by_category(cat.value)
