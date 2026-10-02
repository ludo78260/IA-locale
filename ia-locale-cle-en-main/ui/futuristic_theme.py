#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
futuristic_theme.py - Thème cyberpunk / glassmorphism pour Gradio V2
"""
import gradio as gr

def get_theme():
    """Retourne le thème Gradio."""
    try:
        # Gradio 4.44+ : theme custom
        theme = gr.themes.Soft(
            primary_hue="cyan",
            secondary_hue="violet",
            neutral_hue="slate",
            radius_size="lg",
            font=[gr.themes.GoogleFont("JetBrains Mono"), "monospace"],
        )
        # Custom CSS glassmorphism
        theme.set(
            body_background_fill="*neutral_50",
            body_background_fill_dark="*neutral_950",
            block_background_fill="*neutral_100",
            block_background_fill_dark="*neutral_900",
        )
        return theme
    except Exception:
        return gr.themes.Default()

# CSS additionnel pour effet futuristic
CUSTOM_CSS = """
/* Glassmorphism + cyberpunk */
.gradio-container {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%) !important;
}
.gr-button-primary {
    background: linear-gradient(90deg, #00d4ff, #7c3aed) !important;
    border: none !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.3) !important;
}
.gr-button-primary:hover {
    box-shadow: 0 0 30px rgba(0,212,255,0.5) !important;
    transform: translateY(-1px);
}
.gr-panel, .gr-box {
    backdrop-filter: blur(10px) !important;
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
.gr-textbox, .gr-dropdown {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
}
#header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(90deg, #00d4ff22, #7c3aed22);
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid #00d4ff33;
}
.status-ok { color: #00ff88; }
.status-warn { color: #ffaa00; }
.status-err { color: #ff4444; }
"""
