import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetsHandler():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open("galleria_arben_following").sheet1  # Open the spreadhseet


    def query_find(self, query):
        output = ''
        try:
            q = self.sheet.findall(query)
            for i in q:
                data = self.sheet.row_values(i.row)
                col = ['Cотрудник','Дата','Всего звонков','Продажи','назначено встреч','Бензин','Замечания']
                j = 0
                for i in data:
                    col_name = '<b>' + col[j]  + ': ' + '</b>'
                    j+=1
                    output += col_name + i + '\n'
                output += '\n' + '******************************************' + '\n'
            return output
        except:
            return 'Такого результата нет!'

    def query_add(self, query):
        query = query.split(',')
        for i in range(2, 6):
            query[i] = int(query[i])

        self.sheet.append_row(query)

    def query_update(self, query):
        query = query.split(',')
        self.sheet.update('F6', int(query[1]))

    def query_delete(self, query):
        query = query.split(',')
        self.sheet.append_row(query)