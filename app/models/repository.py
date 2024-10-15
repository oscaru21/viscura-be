from abc import ABC, abstractmethod
from typing import List

class Repository(ABC):
    @abstractmethod
    def search(self, embedding) -> List[int]:
        pass