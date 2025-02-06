from abc import ABC, abstractmethod

class Parser(ABC):

    def __init__(self):
        return None

    @abstractmethod
    def parse(self, s, first, last ):
        
        return s

        