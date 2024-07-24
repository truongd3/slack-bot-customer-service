import re

def split(text):
    '''
    Company Number --> [Company, Number]
    "Company A" Number --> [Company A, Number]
    Company A Number --> [Company A, Number]
    '''
    # Use regex to match a quoted company name and a number or an unquoted company name and a number
    if len(text) == 0:
        return []
    elif " " not in text:
        return [text]
    
    match = re.match(r'\"(.+?)\"\s+([\d\.]+)|(.+?)\s+([\d\.]+)', text)
    if match:
        if match.group(1) and match.group(2):
            return [match.group(1), match.group(2)]
        else:
            return [match.group(3), match.group(4)]
    else:
        raise ValueError("The input text format is incorrect.")