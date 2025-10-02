#Main Controller

from typing import Dict, List, Optional, Union, Any
from pathlib import Path
from uuid import uuid4

from .core.logging import get_logger
from .sources.unified_loader import UnifiedLoader
from .preprocessing.text_preprocessor import TextPreprocessor
from .storage.dataset_exporter import DatasetExporter
from .models import Document, Dataset, TrainingExample

logger = get_logger("training_data_bot")

#laoding, processing, exporting data
class TrainingDataBot:

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.loader = UnifiedLoader()
        self.preprocessor = TextPreprocessor(chunk_size=self.config.get("chunk_size", 512))
        self.exporter = DatasetExporter()
        self.documents: Dict[str, Document] = {}
        self.datasets: Dict[str, Dataset] = {}

  #load documents from files/directories
    async def load_documents(self, sources: Union[str, Path, List[Union[str, Path]]]) -> List[Document]:
  
        if isinstance(sources, (str, Path)):
            sources = [sources]

        documents = []
        for source in sources:
            docs = await self.loader.load(source)
            for d in docs:
                self.documents[d.id] = d
                documents.append(d)
        return documents

  #split into chunks 
    async def process_documents(self, documents: Optional[List[Document]] = None) -> Dataset:
        
        documents = documents or list(self.documents.values())
        examples = []

        for doc in documents:
            chunks = self.preprocessor.chunk_document(doc)
            for chunk in chunks:
                ex = TrainingExample(
                    input_text=chunk.content,
                    output_text="",  # left blank intentionally
                    task_type="chunking",
                    source_document_id=doc.id
                )
                examples.append(ex)
#package chunks into a dataset
        dataset = Dataset(
            name=self.config.get("dataset_name", "dataset_1"),
            description=self.config.get("dataset_description", "Automatically created dataset"),
            examples=examples,
            total_examples=len(examples)
        )
        self.datasets[dataset.id] = dataset
        return dataset

