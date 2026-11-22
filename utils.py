import re

def preprocess(line : str) -> list[str]:
    ''' line preprocessing to load text '''
    result = line.lower() # lower-casing
    result = re.sub(r'[^\w\s]*', '', result) # removing punctuation and non-word
    return result.split()