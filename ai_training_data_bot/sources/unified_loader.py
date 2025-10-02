from pathlib import Path
from typing import List, Union
from .document_loader import DocumentLoader
from .pdf_loader import PDFLoader
from .web_loader import WebLoader
from ..models import Document, DocumentType

class UnifiedLoader:
    def __init__(self):
        self.document_loader = DocumentLoader()
        self.pdf_loader = PDFLoader()
        self.web_loader = WebLoader()
        self.supported_formats = list(DocumentType)

    async def load(self, source: Union[str, Path]) -> List[Document]:
        loader = self._detect_loader(source)
        if loader is None:
            raise ValueError(f"Unsupported or invalid source: {source}")

        document = await loader.load_single(source)
        return [document]

    def _detect_loader(self, source: Union[str, Path]):
        
        if isinstance(source, str) and source.startswith(('http://', 'https://')):
            return self.web_loader

        
        path = Path(source)
        if not path.exists():
            return None

        suffix = path.suffix.lower().lstrip('.')
        try:
            doc_type = DocumentType(suffix)
        except ValueError:
            return None

        if doc_type == DocumentType.PDF:
            return self.pdf_loader
        elif doc_type in [
            DocumentType.TXT, DocumentType.DOCX, DocumentType.MD,
            DocumentType.HTML, DocumentType.JSON, DocumentType.CSV
        ]:
            return self.document_loader
        else:
