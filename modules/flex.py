import gspread
from oauth2client.service_account import ServiceAccountCredentials
from env import FLASK_ENUM

class login_system():
    def __init__(self):
        scope = [
                    'https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive',
                ]

        json_file_name = 'data/sdbtest-405023-ac7947388cf4.json'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
        gc = gspread.authorize(credentials)

        spreadsheet_url = FLASK_ENUM.LINK

        # 스프레스시트 문서 가져오기
        doc = gc.open_by_url(spreadsheet_url)

        # 시트 선택하기
        self.worksheet = doc.worksheet('로그인')

        self.inform_num = self.worksheet.row_count

        self.id_inform = []

    def login(self,id,password):
        self.login = id
        self.password = password

        for i in range(self.inform_num):
            if self.login == self.worksheet.acell(f'C{i+1}').value and self.password == self.worksheet.acell(f'D{i+1}').value:
                self.id_inform.append([self.worksheet.acell(f'E{i+1}').value, self.worksheet.acell(f'B{i+1}').value])
                print(self.id_inform)
                break
                
            else:
                pass

        return self.id_inform



