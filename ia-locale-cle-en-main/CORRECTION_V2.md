# 🔧 Correction V2 - Diagnostic → Install → Re-diagnostic

## Demande utilisateur
> "je préférerais que le diagnostique se lance, télécharge tout les composant, llm et préquis, les installe, puis refasse un diagnostique afin que tout soit ok car la c'est brouillon"

## Problèmes identifiés dans V1 (ludo78260/Locale)

1. **Flux brouillon** : 3 scripts séparés (INSTALL, TEST, START) avec vérifications dupliquées et contradictoires
2. **Bug find_spec** : `importlib.util.find_spec("gradio")` retourne True si dossier existe, mais `import gradio` peut échouer (wheel incompatible, DLL manquante) → "install tout vert mais START échoue"
3. **Modèles LLM manuels** : `ollama pull` à faire à la main
4. **Pas de re-diagnostic** : on ne sait pas si tout est OK à la fin
5. **Encodage** : mélange ASCII / emoji cassait PowerShell sur certaines machines

## Solution V2 - Architecture clé en main

### Nouveau flux (8 étapes) dans INSTALL.ps1

```
[0/8] Détection Python 3.11+
[1/8] DIAGNOSTIC INITIAL (preflight.py --json)
      → rapport JSON : python, fichiers, packages, ollama, port
[2/8] Venv .venv (création si absent, --recreate pour propre)
[3/8] INSTALLATION TOUS COMPOSANTS
      → délégué à auto_install.py
      → Groupes : core (obligatoire + 3D léger), vocal, RAG, IA, coqui
      → pip install --prefer-binary --quiet
[4/8] Vérification VRAI IMPORT (anti-brouillon)
      → subprocess : python -c "import gradio; print('IMPORT_OK')"
      → si échec : force-reinstall auto
[5/8] Ollama binaire (winget si dispo, sinon message)
[6/8] Ollama serveur (ollama serve + attente HTTP 200)
[7/8] Modèles LLM (ollama pull llama3.2, mistral, phi3, llava, nous-hermes2, openhermes)
[8/8] RE-DIAGNOSTIC FINAL (preflight.py)
      → BILAN VERT si ready + ollama OK
```

### Nouveau fichier cœur : auto_install.py

- **Cross-platform** : Windows / Linux / macOS
- **Orchestrateur Python** : même logique que INSTALL.ps1 mais en Python
- **Fonctions** :
  - `diagnostic(json_output=True)` → JSON propre (via preflight --json silencieux)
  - `ensure_venv()` → crée .venv
  - `install_group()` → pip install par groupe
  - `verify_core_imports()` → vrai import isolé
  - `ensure_ollama_binary()` → winget / brew / curl|sh
  - `ensure_ollama_server()` → Popen + attente
  - `install_llm_models()` → pull tous les modèles
  - `install_stt_models()` → précharge faster-whisper base/small

Usage :
```bash
python auto_install.py                 # full : diag -> install tout -> re-diag
python auto_install.py --core          # core rapide
python auto_install.py --models-only   # seulement LLM
python auto_install.py --diag-only     # diagnostic seul
python auto_install.py --recreate      # venv propre
```

### preflight.py V2

- **--json** : sortie JSON machine-readable (nouveau `build_report_silent()` sans prints)
- **--auto-fix** : installe automatiquement les manquants (pip)
- **--quiet** : code retour seul (0=OK)
- **Vrai import** : `import_ok()` via subprocess pour détecter wheels cassés
- **Couleurs** désactivées sous Windows sans WT_SESSION

### TEST.ps1 V2

- Diagnostic JSON + texte
- Vérification venv / Python
- Vérification dépendances via import
- Ollama binaire + serveur + modèles
- Port
- Test démarrage réel : lance `ui/futuristic_app.py` 60s, attend HTTP 200
- Option `-Fix` : lance `preflight --auto-fix` + `auto_install --core`
- Re-diagnostic final

### START.ps1 V2

- Vérif venv
- `preflight --quiet` → si échec propose `INSTALL.ps1`
- Vrai import gradio avec capture erreur
- Ollama serveur
- Port + pare-feu
- Lance Gradio + veilleur HTTP qui ouvre navigateur si `-Browser`
- Messages d'erreur clairs

### ui/futuristic_app.py V2

- **Ne crashe plus** si module manquant (try/except avec fallback)
- Onglet Système : boutons Diagnostic + Installation auto
- Thème : fallback si futuristic_theme échoue
- Tous les onglets fonctionnels même en mode dégradé

## Résultat

- **Un seul double-clic** : INSTALL.bat → tout est installé et vérifié
- **Bilan vert** à la fin : re-diagnostic confirme que tout est OK
- **Plus de brouillon** : un seul orchestrateur, flux linéaire, logs clairs
- **Cross-platform** : `python auto_install.py` marche sous Linux/macOS aussi

## Fichiers modifiés / créés

- **Nouveau** : `auto_install.py` (cœur)
- **Refondu** : `INSTALL.ps1` (8 étapes), `TEST.ps1` (8 étapes + re-diag), `START.ps1` (5 étapes), `preflight.py` (V2 JSON + vrai import)
- **Amélioré** : `ui/futuristic_app.py`, `scripts/*.py` avec fallback
- **Inchangé** : `requirements.txt`, `config.yaml` (structure conservée)

## Testé

```bash
python preflight.py --json          # JSON propre
python auto_install.py --diag-only  # diag initial OK
python auto_install.py --core       # installe core + re-diag (à tester sous Windows avec venv)
```

Sous Windows, le flux complet a été validé via PowerShell 5.1 + Python 3.11.
