from csv import writer
import re,os

def query_find(query):
    result = []
    with open('staff.csv', "r+", encoding='utf8') as f:
        # gives you a list of the lines
        values = f.readlines()
        for i in values:
            find = re.findall(r"\b{}\b".format(query), i, flags=re.IGNORECASE)
            if find:
                result.append(i)
        return result

def append_list_as_row(queries):
    # Open file in append mode

    with open('staff.csv', 'a+', newline='', encoding='utf8') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        for i in queries:
            csv_writer.writerow([i])

