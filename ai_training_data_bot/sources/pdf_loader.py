import asyncio
from pathlib import Path
from typing import List
import fitz  # PyMuPDF

from ..models import Document
from .base_loader import BaseLoader
from ..core.exceptions import DocumentLoadError


class PDFLoader(BaseLoader):

    async def load(self, source) -> List[Document]:
        path = Path(source)
        if path.is_dir():
            return await self._load_directory(path)
        elif path.suffix.lower() == ".pdf":
            return [await self._load_file(path)]
        else:
            raise DocumentLoadError(f"Unsupported source type: {source}")

    async def _load_directory(self, directory: Path) -> List[Document]:
        docs = []
        for pdf_file in directory.rglob("*.pdf"):
            try:
                doc = await self._load_file(pdf_file)
                docs.append(doc)
            except DocumentLoadError:
                continue  # Skip files that fail to load
        return docs

    async def _load_file(self, path: Path) -> Document:
        try:
            def extract_text():
                doc = fitz.open(path)
                text_parts = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.strip():
                        text_parts.append(f"Page {page_num + 1}:\n{text}")
                doc.close()
                return "\n\n".join(text_parts)

            content = await asyncio.to_thread(extract_text)

            return Document(
                title=path.stem,
                content=content,
                source=str(path),
                doc_type="pdf",
                word_count=len(content.split())
            )

        except Exception as e:
            raise DocumentLoadError(f"Failed to load PDF: {path}") from e
