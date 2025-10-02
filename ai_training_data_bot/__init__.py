
__version__ = "3.4.0"
__author__ = "Chase Beck"
__email__ = "chase.b3ck@gmail.com"


#core
from .bot import TrainingDataBot
from .core.config import settings
from .core.logging import get_logger
from .core.logging import get_logger
from .core.exceptions import TrainingDataBotError

#sources
from .sources import PDFLoader, WebLoader, DocumentLoader, UnifiedLoader

#tasks
from .tasks import QAGenerator, ClassificationGenerator, SummarizationGenerator, TaskTemplate

#service
from .decodo import DecodoClident
from .preprocessing import TextPreprocessor
from .evaluation import QualityEvaluator
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

