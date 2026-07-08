# """Application configuration and settings."""

# import os
# from pathlib import Path

# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except ImportError:
#     pass

# BASE_DIR = Path(__file__).resolve().parent.parent
# STORAGE_DIR = BASE_DIR / "storage"
# UPLOADS_DIR = STORAGE_DIR / "uploads"
# VECTORSTORES_DIR = STORAGE_DIR / "vectorstores"

# UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
# VECTORSTORES_DIR.mkdir(parents=True, exist_ok=True)

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
# EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# CHUNK_SIZE = 1000
# CHUNK_OVERLAP = 150
# RETRIEVER_K = 4

# MAX_UPLOAD_MB = 25
# ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]







"""Application configuration and settings."""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
VECTORSTORES_DIR = STORAGE_DIR / "vectorstores"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORES_DIR.mkdir(parents=True, exist_ok=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
RETRIEVER_K = 4

MAX_UPLOAD_MB = 25

_default_origins = "http://localhost:5173,http://127.0.0.1:5173"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", _default_origins).split(",")
