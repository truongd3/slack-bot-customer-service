import re
import csv

db = "CustomerList.csv"

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
    
def get_data_to_prompt():
    pre_prompt = ""
    with open(db, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rate = -1 if int(row["Rates"]) == 0 else float(row["SumRating"]) / int(row["Rates"])
            if rate == -1:
                pre_prompt += ("Company " + row["Company"] + " does " + row["ServiceType"] + " and does not have any rate yet; ")
            else:
                pre_prompt += ("Company " + row["Company"] + " does " + row["ServiceType"] + " and its rating is " + str(rate) + " from " + row["Rates"] + " users; ")
            pre_prompt += "they offer " + row["Discount"] + f"% discount for Justworks employees.\n"
    return pre_prompt