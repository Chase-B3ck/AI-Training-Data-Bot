import json
import asyncio
from pathlib import Path
from typing import List
from ..models import Document
from .base_loader import BaseLoader
from ..core.exceptions import DocumentLoadError

class DocumentLoader(BaseLoader):
    """
    Loads text-based documents from files or directories.
    Supports TXT, MD, HTML, JSON, and CSV formats.
    """

    async def load(self, source) -> List[Document]:
        path = Path(source)
        if path.is_dir():
            return await self._load_directory(path)
        else:
            return [await self._load_file(path)]

    async def _load_directory(self, directory: Path) -> List[Document]:
        supported = ['*.txt', '*.md', '*.json', '*.csv', '*.html']
        docs = []
        for pattern in supported:
            for p in directory.rglob(pattern):
                try:
                    docs.append(await self._load_file(p))
                except DocumentLoadError as e:
                    # Log or skip failed files
                    continue
        return docs

    async def _load_file(self, path: Path) -> Document:
        ext = path.suffix.lower().lstrip('.')
        try:
            if ext in ('txt', 'md', 'html', 'csv'):
                content = await asyncio.to_thread(path.read_text, encoding='utf-8', errors='ignore')
            elif ext == 'json':
                raw = await asyncio.to_thread(path.read_text, encoding='utf-8')
                content = json.dumps(json.loads(raw), ensure_ascii=False)
            else:
                raise DocumentLoadError(f"Unsupported file type: {ext}")
        except Exception as e:
            raise DocumentLoadError(f"Failed to load file: {path}") from e

        return Document(
            title=path.stem,
            content=content,
            source=str(path),
            doc_type=ext,
            word_count=len(content.split())
        )
