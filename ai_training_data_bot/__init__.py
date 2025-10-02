
__version__ = "3.4.0"
__author__ = "Chase Beck"
__email__ = "chase.b3ck@gmail.com"


from .bot import TrainingDataBot
from .core.logging import get_logger
from .storage.dataset_exporter import DatasetExporter

__all__ = [
    # Core
    "TrainingDataBot", "settings", "get_logger", "TrainingDataBotError",

    # Sources
    "PDFLoader", "WebLoader", "DocumentLoader", "UnifiedLoader",

    # Tasks
    "QAGenerator", "ClassificationGenerator", "SummarizationGenerator", "TaskTemplate",

    # Services
    "DecodoClient", "TextPreprocessor", "QualityEvaluator", "DatasetExporter"

