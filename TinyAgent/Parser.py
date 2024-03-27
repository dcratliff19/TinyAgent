from abc import ABC, abstractmethod


class Parser(ABC):

    def __init__(self):
        return None
    
    @abstractmethod
    def json_parse(self, string, first, last):
        try:
            start = string.index( first ) + len( first )
            end = string.rfind( last, 0 )
            return string[start:end]
        
        except ValueError:
            return "Invalid JSON string - " + string

    @abstractmethod
    def parse(self, s, first, last ):
        
        return self.json_parse(s, first, last)

        