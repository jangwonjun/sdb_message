import gspread
from oauth2client.service_account import ServiceAccountCredentials

class candidate_data():
    def __init__(self,url):
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
        self.url = url
    

        json_file_name = 'data/sdbtest-405023-ac7947388cf4.json'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
        gc = gspread.authorize(credentials)

        spreadsheet_url = self.url

        # 스프레스시트 문서 가져오기
        doc = gc.open_by_url(spreadsheet_url)

        # 시트 선택하기
        worksheet_1 = doc.worksheet('학습일지')
        worksheet_2 = doc.worksheet('전송인원정보')
        self.worksheet_3 = doc.worksheet('전송메세지')
        worksheet_4 = doc.worksheet('주관관리표')
        
        #num_inf는 출력할 학생수를 의미한다!
        
        self.num_inf = worksheet_2.acell('C5').value
        
        # 범위(셀 위치 리스트) 가져오기
        range_list = worksheet_1.range(f'A2:M{int(self.num_inf)+1}')
        
        #상속처리하자!
        self.index_num = worksheet_1.row_count

        # 범위에서 각 셀 값 가져오기
        for cell in range_list:
            message.append(cell.value)

        #',' 단위로 나누기!
        for i in range(len(message)):
            message1.extend(list(filter(None, message[i].split(','))))

        interval = 13
        inform_student = []

        for i in range(0,len(message1),interval):
            temp_slice = message1[i:i+interval]
            inform_student.append(list(filter(None,temp_slice)))

        #이름 : inform_student[0][2]
        
        #print(inform_student[5])

       
        for i in range(int(self.num_inf)):
            message = f"안녕하세요! 어머니 수다방 수학학원 하웅진T 입니다. 금일 수업 진행상황 알려드립니다!\n[수업내용]\n\n{inform_student[i][4]}\n\n[교재]\n\n{inform_student[i][5]}"

            self.worksheet_3.update(f'A{i+2}',inform_student[i][2])
            self.worksheet_3.update(f'C{i+2}',message)
            self.result.append([message, inform_student[i][2]])

        print("Sheet3 전송메세지 정리완료...")


    def send_student_num(self):
        #print("전송할 학생 숫자를 입력받고 넘김 ㅋ")
        return self.num_inf
    
    def send_student_message(self):
        #무조건 전송해야할값들
        #print("학생들의 멘트 넘김.")
        self.data = []
        for i in range(int(self.num_inf)):
            send_message = self.worksheet_3.acell(f'C{i+2}').value
            send_student_name = self.worksheet_3.acell(f'A{i+2}').value
            #print(send_message,send_student_name)
            #print(i)
            self.data.append([send_message,send_student_name])
        
        print("Sheet3 기반 전송메세지 저장완료...")
        return self.data


    def search_phone_num_student(self):
        with open('data/sdb_student_db.csv',encoding='utf-8') as f:
            sdb_db = f.read()
            
        data_list = [line.split(',') for line in sdb_db.split('\n')]
        data_list[0][0] = data_list[0][0].lstrip('\ufeff')
        
        #print(len(data_list))

        for p in range(len(data_list)):
            for i in range(int(self.num_inf)):
                if data_list[p][0] == self.result[i][1]:
                    #학생이름을 통해 학생 전화번호 찾기
                    #print(data_list[p][3])
                    #중복방지작업_1차안 마련해야함. 일단 진행하기

                    #[학생전화번호,부모님전화번호,이름] 배열로 저장
                    self.send_num_student.append([data_list[p][3],data_list[p][4],data_list[p][0]])
        
        
        print("1차 데이터 정리완료...")
            
            
        
        for p in range(int(self.num_inf)):
            for i in range(len(self.send_num_student)):
                if self.result[p][1] == self.send_num_student[i][2]:
                    self.send_num_student[i].insert(3, self.result[p][0])
    
        print("2차 데이터 정리완료...")
        
        print(self.send_num_student)
        
        return self.send_num_student
    
  


    
        
