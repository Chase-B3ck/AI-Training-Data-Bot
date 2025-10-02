from dataclasses import dataclass, field
from uuid import uuid4, UUID
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum


class TaskType(str, Enum):
    QA_GENERATION = "qa_generation"
    CLASSIFICATION = "classification"
    SUMMARIZATION = "summarization"
    NER = "named_entity_recognition"
    RED_TEAMING = "red_teaming"
    INSTRUCTION_RESPONSE = "instruction_response"

class ExportFormat(str, Enum):
    JSONL = "jsonl"
    CSV = "csv"

@dataclass
class BaseEntity:
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
  
@dataclass
class Document(BaseEntity):
    title: str = ""
    content: str = ""
    source: str = ""
    doc_type: str = ""
    word_count: int = 0

@dataclass
class TextChunk(BaseEntity):
    document_id: UUID = field(default_factory=uuid4)
    content: str = ""
    start_index: int = 0
    end_index: int = 0
    chunk_index: int = 0
    token_count: int = 0


