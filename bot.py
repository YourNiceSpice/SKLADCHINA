from sheets import SheetsHandler
from work_with_csv_sheet import query_find

def finder(message):
    """
    find all entries
    """
    find = SheetsHandler()

    result = find.query_find(message)
    q = 1
    return result

def finder_csv(message):
    """
    find all entries
    """

    result = query_find(message)
    return result




message = input("Введите что-нибудь, чтобы проверить это: \n")
output = finder_csv(message)
print(output)