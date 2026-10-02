# 🤖 IA Locale — Assistant IA 100% local — V2 Clé en main

> **Correction majeure demandée :**  
> *"je préférerais que le diagnostique se lance, télécharge tout les composant, llm et préquis, les installe, puis refasse un diagnostique afin que tout soit ok car la c'est brouillon"*

**C'est fait.** Le projet a été refondu en flux **Diagnostic → Installation totale → Re-diagnostic**.

Interface web (Gradio) qui regroupe **reconnaissance vocale, synthèse vocale, RAG, génération d'images, 3D, personnalités, monitoring système et nettoyage automatique** — le tout exécuté sur votre machine, sans compte ni service en ligne.

---

## 🚀 Démarrage en 3 étapes - V2 Clé en main

| Étape | Action | Ce qu'il se passe (nouveau flux) |
|-------|--------|-----------------------------------|
| **1** | Double-cliquez sur **`INSTALL.bat`** | **1. Diagnostic initial** (preflight.py --json) → **2. Création venv** → **3. Installation de TOUS les composants** (core + vocal + RAG + IA + 3D + TTS) → **4. Vérification vrai import** → **5. Installation Ollama** → **6. Démarrage serveur** → **7. Téléchargement modèles LLM** (llama3.2, mistral, phi3, llava, nous-hermes2, openhermes) → **8. Re-diagnostic final VERT** |
| **2** | Double-cliquez sur **`TEST.bat`** | Vérifie que tout est prêt, teste le démarrage réel de l'interface, option `-Fix` pour auto-corriger |
| **3** | Double-cliquez sur **`START.bat`** | Lance l'interface. Option `-Browser` : ouvre le navigateur automatiquement |

Puis ouvrez : **http://127.0.0.1:7860**

> Le démarrage peut prendre 30-90s (plus au 1er lancement) : la console affiche l'avancement.

> En ligne de commande : `.\INSTALL.ps1`, `.\TEST.ps1`, `.\START.ps1` ou `python auto_install.py`

---

## 🆕 Quoi de neuf V2 vs V1 brouillon ?

### Problème V1 :
- INSTALL, TEST, START faisaient des vérifications séparées, parfois contradictoires
- `find_spec` détectait un dossier mais pas un wheel cassé → "install tout vert mais START échoue sur gradio"
- Modèles LLM à installer manuellement
- Pas de re-diagnostic final

### Solution V2 :
1. **Orchestrateur central `auto_install.py`** :
   - Python pur, cross-platform (Windows/Linux/macOS)
   - Flux : `diagnostic(initial) → install(tout) → diagnostic(final)` 
   - Sortie JSON pour automatisation
   - Détection wheels cassés par **vrai import isolé** (`subprocess` + `importlib.import_module`)

2. **INSTALL.ps1 refondu** :
   - 8 étapes claires avec `Write-Step`
   - Délègue à `auto_install.py` pour la logique lourde
   - Re-diagnostic final obligatoire → bilan VERT

3. **preflight.py V2** :
   - `--json` pour machine-readable
   - `--auto-fix` pour auto-install pip
   - Vérification vrai import (corrige bug gradio)

4. **TEST.ps1 V2** :
   - Diagnostic JSON + texte
   - Test HTTP réel
   - Option `-Fix` qui lance `auto_install --core`

5. **Interface Gradio** :
   - Onglet Système avec bouton "Diagnostic" et "Installation auto"
   - Ne crashe plus si module manquant (fallback)

---

## 📋 Prérequis

| Logiciel | Version | Où |
|----------|---------|-----|
| **Python** | 3.11 (3.12 accepté) | https://www.python.org/downloads/windows/ — cochez **Add python.exe to PATH** |
| **Ollama** | dernière | https://ollama.com/download — **auto-installé par INSTALL.ps1 via winget** |

Git / Visual C++ Build Tools : **Plus requis** (roues précompilées).

---

## 🧩 Contenu du projet V2

```
ia-locale-cle-en-main/
├── INSTALL.bat / INSTALL.ps1     # V2 : diag -> install tout -> re-diag (8 étapes)
├── START.bat   / START.ps1       # V2 : vérif + ollama + port + launch
├── TEST.bat    / TEST.ps1        # V2 : diag JSON + test HTTP + re-diag
├── auto_install.py               # NOUVEAU : orchestrateur clé en main (cœur de la correction)
├── preflight.py                  # V2 : --json, --auto-fix, vrai import
├── install_all_ai.py             # V2 : wrapper autour de auto_install.py
├── requirements.txt              # Toutes dépendances
├── requirements-core.txt         # Dépendances minimales
├── config/
│   ├── config.yaml               # Config principale (port, modèles)
│   └── personalities/            # 8 personnalités
├── ui/
│   ├── futuristic_app.py         # V2 : ne crashe plus si module manquant + onglet Système
│   └── futuristic_theme.py       # Thème cyberpunk
├── scripts/                      # Modules fonctionnels V2
│   ├── project_paths.py
│   ├── llm.py                    # Ollama chat + list
│   ├── tts.py                    # Piper / Coqui avec fallback
│   ├── stt.py                    # faster-whisper
│   ├── rag.py                    # ChromaDB + embeddings
│   ├── ai_model_manager.py       # Catalogue modèles
│   ├── llm_checker.py
│   ├── personality_manager.py
│   ├── resource_monitor.py
│   ├── auto_cleaner.py
│   ├── sound_effects.py
│   ├── advanced_voice_commands.py
│   └── dictation_mode.py
├── 3d/                           # Génération 3D
├── models/                       # Créé à l'usage (piper, etc)
├── outputs/                      # Images, audio générés
└── chroma_db/                    # Base vectorielle RAG
```

---

## 🔧 Usage avancé

### Python direct (cross-platform)

```bash
# Diagnostic seul
python preflight.py
python preflight.py --json

# Installation clé en main complète
python auto_install.py
# = diag initial -> venv -> all deps -> ollama -> modèles LLM -> re-diag final

# Options
python auto_install.py --core        # core uniquement (rapide)
python auto_install.py --no-models   # sans LLM
python auto_install.py --models-only # seulement ollama pull
python auto_install.py --diag-only   # diagnostic seul
python auto_install.py --recreate    # recrée venv

# Wrapper legacy
python install_all_ai.py --list
python install_all_ai.py --category llm
```

### PowerShell

```powershell
.\INSTALL.ps1 -Core          # rapide
.\INSTALL.ps1 -Recreate      # venv propre
.\INSTALL.ps1 -NoModels      # sans LLM
.\INSTALL.ps1 -DiagOnly      # diagnostic seul

.\TEST.ps1 -Fast             # sans test HTTP
.\TEST.ps1 -Fix              # auto-fix
.\TEST.ps1 -IA               # + simulation IA

.\START.ps1 -Browser         # ouvre navigateur
.\START.ps1 -Port 8080       # port custom
.\START.ps1 -SkipChecks      # ignore verifs
```

---

## ✨ Fonctionnalités

- **Chat LLM** : llama3.2, mistral, phi3, llava, nous-hermes2, openhermes (via Ollama)
- **STT** : faster-whisper (temps réel, FR)
- **TTS** : Piper (léger) + Coqui (qualité) - 100% local
- **RAG** : PDF, DOCX, TXT → ChromaDB + sentence-transformers
- **Images** : Stable Diffusion (diffusers)
- **3D** : trimesh + scikit-image → export STL/3MF/OBJ/PLY/GLB
- **Personnalités** : 8 profils + création
- **Non censuré** : onglet dédié 🌙/🌑
- **Système** : monitoring, nettoyage, diagnostic intégré

---

## 🐛 Dépannage V2

| Symptôme | Solution V2 |
|----------|-------------|
| `gradio` présent mais import échoue | Corrigé : `auto_install.py` fait vrai import + force-reinstall auto. Sinon `INSTALL.ps1 -Recreate -Core` |
| Ollama non trouvé | `INSTALL.ps1` installe via winget, ou https://ollama.com/download |
| Port 7860 utilisé | `START.ps1 -Port 8080` ou fermer ancienne instance |
| Modèles LLM manquants | `python auto_install.py --models-only` ou `ollama pull llama3.2` |
| Venv corrompu | `INSTALL.ps1 -Recreate` |
| Diagnostic final rouge | Voir `TEST.ps1 -Fix` ou `preflight.py --fix` |

---

## 📜 Licence

Projet local, 100% offline. Aucune donnée envoyée.

---

**V2 - Flux clé en main : Diagnostic → Install tout (composants + LLM + prérequis) → Re-diagnostic → OK**
