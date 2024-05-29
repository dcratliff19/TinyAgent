from TinyAgent.abstracts import Parser

class jsonOutputParser(Parser):

    def __init__(self):
        super().__init__()
    
    def parse(self, string, first, last):
        try:
            
            cleaned_string = string.replace("json", "").replace("\\", "")
            start = cleaned_string.index( first ) + len( first )
            end = cleaned_string.rfind( last, 0 )
            return cleaned_string[start:end]
        
        except ValueError:
            return "Invalid JSON string - " + string


        