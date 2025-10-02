from typing import List
from ..models import Document, TextChunk
from uuid import uuid4
from ..core.logging import get_logger

class TextPreprocessor:
    def __init__(self, chunk_size: int = 512):
        self.chunk_size = chunk_size
        self.logger = get_logger("text_preprocessor")

    def chunk_document(self, document: Document) -> List[TextChunk]:
        self.logger.debug(f"Chunking document: {document.title} (ID: {document.id})")

        words = document.content.split()
        chunks = []
        i = 0
        chunk_index = 0

        while i < len(words):
            chunk_words = words[i:i + self.chunk_size]
            content = ' '.join(chunk_words)

            chunk = TextChunk(
                id=uuid4(),
                document_id=document.id,
                content=content,
                start_index=i,
                end_index=i + len(chunk_words),
                chunk_index=chunk_index,
                token_count=len(chunk_words)
            )

            chunks.append(chunk)
            self.logger.debug(f"Created chunk {chunk_index} with {len(chunk_words)} tokens")

            i += self.chunk_size
            chunk_index += 1

        self.logger.info(f"Finished chunking document: {len(chunks)} chunks created")
        return chunks
