from pathlib import Path
from typing import List, Union
from .document_loader import DocumentLoader
from .pdf_loader import PDFLoader  # Assuming this is implemented
from ..models import Document, DocumentType

class UnifiedLoader:
    def __init__(self):
        self.document_loader = DocumentLoader()
        self.pdf_loader = PDFLoader()
        self.supported_formats = [DocumentType.TXT, DocumentType.DOCX, DocumentType.PDF]

    async def load(self, source: Union[str, Path]) -> List[Document]:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Source not found: {source}")

        doc_type = self._detect_type(path)
        if doc_type == DocumentType.PDF:
            return [await self.pdf_loader.load_single(path)]
        elif doc_type in [DocumentType.TXT, DocumentType.DOCX]:
            return [await self.document_loader.load_single(path)]
        else:
            raise ValueError(f"Unsupported document type: {doc_type}")

    def _detect_type(self, path: Path) -> DocumentType:
        suffix = path.suffix.lower().lstrip('.')
        try:
            return DocumentType(suffix)
        except ValueError:
            raise ValueError(f"Unknown file extension: {suffix}")
