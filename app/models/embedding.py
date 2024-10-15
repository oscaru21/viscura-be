from abc import ABC, abstractmethod
import numpy as np

class Embedding(ABC):
    @abstractmethod
    def transform(self, X) -> np.ndarray:
        pass