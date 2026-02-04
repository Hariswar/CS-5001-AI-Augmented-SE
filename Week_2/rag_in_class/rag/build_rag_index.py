#!/usr/bin/env python3
"""
Build a FAISS RAG index over:
- dataset/outputs/tasks/task_*.py          (refactored code)
- dataset/outputs/error_logs/*.txt         (pytest logs)
- dataset/input/tests/test_task_*.py       (tests, optional but recommended)

Writes:
- dataset/outputs/rag_faiss_index/         (FAISS index + metadata)

Requirements:
  pip install langchain langchain-community langchain-ollama faiss-cpu
  ollama pull nomic-embed-text
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass(frozen=True)
class Paths:
    dataset_root: Path
    refactored_tasks_dir: Path
    error_logs_dir: Path
    tests_dir: Path
    index_dir: Path


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def load_docs(paths: Paths) -> List[Document]:
    docs: List[Document] = []

    if paths.refactored_tasks_dir.exists():
        for p in sorted(paths.refactored_tasks_dir.glob("task_*.py")):
            docs.append(Document(page_content=read_text(p), metadata={"source": str(p), "type": "code"}))

    if paths.error_logs_dir.exists():
        for p in sorted(paths.error_logs_dir.glob("*.txt")):
            docs.append(Document(page_content=read_text(p), metadata={"source": str(p), "type": "error_log"}))

    if paths.tests_dir.exists():
        for p in sorted(paths.tests_dir.glob("test_task_*.py")):
            docs.append(Document(page_content=read_text(p), metadata={"source": str(p), "type": "test"}))

    return docs


def main() -> None:
    dataset_root = Path("dataset").resolve()
    paths = Paths(
        dataset_root=dataset_root,
        refactored_tasks_dir=dataset_root / "outputs" / "tasks",
        error_logs_dir=dataset_root / "outputs" / "error_logs",
        tests_dir=dataset_root / "input" / "tests",
        index_dir=dataset_root / "outputs" / "rag_faiss_index",
    )

    docs = load_docs(paths)
    if not docs:
        raise SystemExit("No documents found to index. Check dataset/outputs/tasks and dataset/outputs/error_logs.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    embed_model = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    embeddings = OllamaEmbeddings(model=embed_model)

    vectordb = FAISS.from_documents(chunks, embeddings)

    paths.index_dir.mkdir(parents=True, exist_ok=True)
    vectordb.save_local(str(paths.index_dir))


if __name__ == "__main__":
    main()

