import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

class SheetsHandler():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open("galleria_arben_following").sheet1  # Open the spreadhseet


    def query_find(self, query):
        result = []
        values = self.sheet.get_all_values()
        for i in values:
            find = re.findall(r"\b{}\b".format(query), i[0])
            if find:
                result.append(i[0])
        if result:
            return result
        else:
            return 'По этому запросу ничего нет'


    def query_add(self, queries):

        self.sheet.append_rows([queries])

    def query_update(self, query):
        query = query.split(',')
        self.sheet.update('F6', int(query[1]))

    def query_delete(self, query):
        query = query.split(',')
        self.sheet.append_row(query)