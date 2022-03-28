import re

class StringManipulator:
    def remove_punctuation(str):
        return re.sub(r'[^\w\s]', "", str)
    
    def remove_spaces(str):
        return re.sub('\s+', "", str)

    def remove_quotes(str):
        return str.replace('"' , "")

    def remove_newlines_only(str):
        return str.strip().replace('\n', '')