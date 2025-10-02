from abc import ABC, abstractmethod
from typing import List
from ..models import Document

class BaseLoader(ABC):
    @abstractmethod
    async def load(self, source) -> List[Document]:
        raise NotImplementedError
