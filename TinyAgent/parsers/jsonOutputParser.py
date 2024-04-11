from abc import ABC, abstractmethod


class jsonOutputParser(ABC):

    def __init__(self):
        return None
    
    @abstractmethod
    def parse(self, string, first, last):
        try:
            start = string.index( first ) + len( first )
            end = string.rfind( last, 0 )
            return string[start:end]
        
        except ValueError:
            return "Invalid JSON string - " + string


        