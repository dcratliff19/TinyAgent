from TinyAgent.abstracts import Parser

class jsonOutputParser(Parser):

    def __init__(self):
        super().__init__()
    
    def parse(self, string, first, last):
        try:
            start = string.index( first ) + len( first )
            end = string.rfind( last, 0 )
            return string[start:end]
        
        except ValueError:
            return "Invalid JSON string - " + string


        