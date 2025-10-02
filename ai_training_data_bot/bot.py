from typing import Dict, List, Optional, Union, Any
from pathlib import Path
from uuid import uuid4
from datetime import datetime


from .core.logging import get_logger
from .core.config import settings
from .core.exceptions import TrainingDataBotError


from .sources.unified_loader import UnifiedLoader
from .preprocessing.text_preprocessor import TextPreprocessor


from .evaluation import QualityEvaluator
from .storage.dataset_exporter import DatasetExporter


from .models import Document, Dataset, TrainingExample, TaskType, ExportFormat

# Initialize logger
logger = get_logger("training_data_bot")

#main controller class 
class TrainingDataBot:
    
#load configuration
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        #load configuration
        self.config = config or {}

        #core components
        self.loader = UnifiedLoader()
        self.preprocessor = TextPreprocessor(chunk_size=self.config.get("chunk_size", 512))
        self.evaluator = QualityEvaluator()
        self.exporter = DatasetExporter()

        #state tracking
        self.documents: Dict[str, Document] = {}
        self.datasets: Dict[str, Dataset] = {}

        logger.info("TrainingDataBot initialized successfully")

    #Load documents with UnifiedLoader
    async def load_documents(self, sources: Union[str, Path, List[Union[str, Path]]]) -> List[Document]:
        
        if isinstance(sources, (str, Path)):
            sources = [sources]

        documents = []
        for source in sources:
            docs = await self.loader.load(source)
            for d in docs:
                self.documents[d.id] = d
                documents.append(d)

        logger.info(f"Loaded {len(documents)} documents")
        return documents

        #chunking logic
    async def process_documents(self, documents: Optional[List[Document]] = None) -> Dataset:
        
        documents = documents or list(self.documents.values())
        examples = []

        for doc in documents:
            chunks = self.preprocessor.chunk_document(doc)
            for chunk in chunks:
                ex = TrainingExample(
                    input_text=chunk.content,
                    output_text="",  # Placeholder for generated output
                    task_type=TaskType.SUMMARIZATION,  # Example task type
                    source_document_id=doc.id
                )
                examples.append(ex)

        #package all examples into a dataset
        dataset = Dataset(
            name=self.config.get("dataset_name", f"dataset_{datetime.utcnow().isoformat()}"),
            description=self.config.get("dataset_description", "Automatically created dataset"),
            examples=examples,
            total_examples=len(examples)
        )
        self.datasets[dataset.id] = dataset

        logger.info(f"Processed {len(examples)} examples into dataset '{dataset.name}'")
        return dataset

    #evaluation of dataset
    async def evaluate_dataset(self, dataset: Dataset, detailed_report: bool = True):
        
        report = await self.evaluator.evaluate_dataset(dataset, detailed_report=detailed_report)
        logger.info(f"Evaluation complete. Passed: {report.passed}")
        return report

    async def export_dataset(
        self,
        dataset: Dataset,
        output_path: Union[str, Path],
        format: ExportFormat = ExportFormat.JSONL,
        split_data: bool = True
    ) -> Path:
        #export dataset
        path = await self.exporter.save(dataset, output_path, format=format, split_data=split_data)
        logger.info(f"Dataset exported to {path}")
        return path

    async def quick_process(
        self,
        source: Union[str, Path],
        output_path: Union[str, Path],
        task_types: Optional[List[TaskType]] = None,
        export_format: ExportFormat = ExportFormat.JSONL
    ) -> Dataset:
        
        documents = await self.load_documents([source])
        dataset = await self.process_documents(documents)
        await self.export_dataset(dataset, output_path, format=export_format)
        return dataset
#system cleanup
    async def cleanup(self):
        
        await self.exporter.close()
        if hasattr(self.evaluator, "close"):
            await self.evaluator.close()
        logger.info("TrainingDataBot cleanup completed")
#autosetup
    async def __aenter__(self):
        
        return self
#autocleanup
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        
        await self.cleanup()
#summary information
    def get_statistics(self) -> Dict[str, Any]:
        
        return {
            "documents": {
                "total": len(self.documents),
                "total_size": sum(doc.word_count for doc in self.documents.values())
            },
            "datasets": {
                "total": len(self.datasets),
                "total_examples": sum(len(ds.examples) for ds in self.datasets.values())
            }
        }
