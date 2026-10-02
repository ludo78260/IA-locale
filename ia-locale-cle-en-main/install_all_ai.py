#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_all_ai.py - Installation complète des IA V2 (clé en main)
==================================================================
Refonte pour répondre à la demande :
  - Diagnostic -> install tout -> re-diagnostic
  - Utilise auto_install.py comme backend propre

Usage:
    python install_all_ai.py              # installe tout (diag -> install -> re-diag)
    python install_all_ai.py --core       # core seulement
    python install_all_ai.py --list       # liste modèles
    python install_all_ai.py --category llm
"""

import argparse
import sys
from pathlib import Path

# Ajoute scripts au path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

try:
    import auto_install
except ImportError as e:
    print(f"Impossible d'importer auto_install : {e}")
    sys.exit(1)

def list_models():
    from scripts.ai_model_manager import list_models as lm
    lm()

def main():
    parser = argparse.ArgumentParser(description="IA Locale - Installation complète IA V2")
    parser.add_argument("--core", action="store_true", help="Core uniquement")
    parser.add_argument("--no-models", action="store_true", help="Sans modèles LLM")
    parser.add_argument("--models-only", action="store_true", help="Seulement modèles")
    parser.add_argument("--category", type=str, help="Catégorie : llm, stt, tts, image, embedding, 3d")
    parser.add_argument("--list", action="store_true", help="Liste modèles")
    parser.add_argument("--diag-only", action="store_true", help="Diagnostic seul")
    parser.add_argument("--recreate", action="store_true", help="Recrée venv")
    args = parser.parse_args()

    if args.list:
        list_models()
        return

    if args.category:
        from scripts.ai_model_manager import install_by_category
        print(f"Installation catégorie : {args.category}")
        install_by_category(args.category)
        return

    # Sinon, délégation à auto_install
    sys.argv = ["auto_install.py"]
    if args.core:
        sys.argv.append("--core")
    if args.no_models:
        sys.argv.append("--no-models")
    if args.models_only:
        sys.argv.append("--models-only")
    if args.diag_only:
        sys.argv.append("--diag-only")
    if args.recreate:
        sys.argv.append("--recreate")

    auto_install.main()

if __name__ == "__main__":
    main()
