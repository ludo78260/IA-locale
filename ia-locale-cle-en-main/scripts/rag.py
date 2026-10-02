#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rag.py - Recherche documentaire (ChromaDB + sentence-transformers)
"""
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

def get_embedding_function():
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return model
    except ImportError:
        return None

def get_chroma_client():
    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        return client
    except ImportError:
        return None

def ingest_file(file_path: str, collection_name: str = "documents"):
    """Ingère un PDF/DOCX/TXT dans Chroma."""
    try:
        import chromadb
        from pathlib import Path
        import pypdf

        text = ""
        fp = Path(file_path)
        if fp.suffix.lower() == ".pdf":
            reader = pypdf.PdfReader(str(fp))
            for page in reader.pages:
                text += page.extract_text() or ""
        elif fp.suffix.lower() in [".txt", ".md"]:
            text = fp.read_text(encoding="utf-8", errors="ignore")
        elif fp.suffix.lower() == ".docx":
            try:
                import docx2txt
                text = docx2txt.process(str(fp))
            except:
                text = ""
        else:
            text = fp.read_text(encoding="utf-8", errors="ignore")

        if not text.strip():
            return False, "Aucun texte extrait"

        # Chunking simple
        chunks = [text[i:i+1000] for i in range(0, len(text), 800)]

        client = get_chroma_client()
        if not client:
            return False, "ChromaDB non installé"

        # Embedding
        emb_model = get_embedding_function()
        if not emb_model:
            return False, "sentence-transformers non installé"

        collection = client.get_or_create_collection(collection_name)
        ids = [f"{fp.name}_{i}" for i in range(len(chunks))]
        embeddings = emb_model.encode(chunks).tolist()

        collection.add(ids=ids, documents=chunks, embeddings=embeddings)
        return True, f"{len(chunks)} chunks ingérés"

    except Exception as e:
        return False, f"Erreur RAG: {e}"

def query(question: str, collection_name: str = "documents", n_results: int = 3) -> str:
    """Interroge la base."""
    try:
        client = get_chroma_client()
        if not client:
            return "RAG non disponible (ChromaDB manquant)"

        emb_model = get_embedding_function()
        if not emb_model:
            return "RAG non disponible (embeddings manquants)"

        collection = client.get_or_create_collection(collection_name)
        q_emb = emb_model.encode([question]).tolist()

        results = collection.query(query_embeddings=q_emb, n_results=n_results)
        docs = results.get("documents", [[]])[0]

        if not docs:
            return "Aucun document pertinent trouvé."

        context = "\n\n".join(docs)
        return f"Contexte trouvé ({len(docs)} docs):\n{context}\n\n---\nQuestion: {question}"

    except Exception as e:
        return f"Erreur RAG query: {e}"

def list_collections():
    client = get_chroma_client()
    if not client:
        return []
    try:
        return [c.name for c in client.list_collections()]
    except:
        return []
