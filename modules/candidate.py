import gspread
from oauth2client.service_account import ServiceAccountCredentials

class candidate_data():
    def __init__(self):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
        ]

        message = []
        self.result = []
        temp = []
        self.target_message = []
        message1 = []
        self.send_num = []
        self.send_num_student = []
        self.send_num_parents = []
        self.send_name_student = []
    

        json_file_name = 'data/sdbtest-405023-ac7947388cf4.json'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
        gc = gspread.authorize(credentials)

        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1oS8bePikNsnO6MIVB38x7Mko_vKR_m0FtmPt4a0xBX0/edit?usp=sharing'

        # 스프레스시트 문서 가져오기
        doc = gc.open_by_url(spreadsheet_url)

        # 시트 선택하기
        worksheet = doc.worksheet('수다방_문자서비스')

        # 범위(셀 위치 리스트) 가져오기
        range_list = worksheet.range('A2:K5')

        self.index_num = worksheet.row_count

        # 범위에서 각 셀 값 가져오기
        for cell in range_list:
            message.append(cell.value)

        for i in range(len(message)):
            # '.'을 기준으로 끊고 빈 문자열 제거하여 리스트로 변환
            message1.extend(list(filter(None, message[i].split('.'))))

        # 날짜의 위치 찾기
        date_index = [i for i, item in enumerate(message1) if '/' in item]

        self.result = [message1[date_index[i-1]:date_index[i]] for i in range(1, len(date_index))]

        self.result.append(message1[date_index[-1]:])

    
    def search_phone_num_student(self):
        with open('data/sdb_student_db.csv',encoding='utf-8') as f:
            sdb_db = f.read()
            
        data_list = [line.split(',') for line in sdb_db.split('\n')]
        data_list[0][0] = data_list[0][0].lstrip('\ufeff')
        
        #print(data_list[0][0])
        
        for i in range(len(data_list)):
            self.send_name_student.append(data_list[i][0])
        
        #print(self.send_name_student)
        
        for p in range(len(data_list)):
            if data_list[p][0] == self.result[p][1]:
                #학생이름을 통해 학생 전화번호 찾기
                #print(data_list[p][3])
                self.send_num_student.append(data_list[p][3])
            
        print("TEST", self.send_name_student)
        
        return self.send_num_student, self.send_name_student # 전화번호 데이터, 이름 데이터 반환
    
    def search_phone_num_parents(self):
        with open('data/sdb_student_db.csv',encoding='utf-8') as f:
            sdb_db_parents = f.read()
            
        parents_data_list = [line.split(',') for line in sdb_db_parents.split('\n')]
        
        #print(data_list[0][0])
        
        for i in range(len(parents_data_list)):
            if parents_data_list[i][0] == self.result[i][1]:
                #학생이름을 통해 부모님 전화번호 찾기
                #print(data_list[i][4])
                self.send_num_parents.append(parents_data_list[i][4])
            
        #print(self.send_num_parents)
        
        return self.send_num_parents, self.result #  학부모 전화번호 데이터 반환
    
        


