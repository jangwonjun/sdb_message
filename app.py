import json
from src.lib import message, storage
import pandas
from env import SEND
from tqdm import tqdm

             
if __name__ == '__main__':
    #print(clean_number())
    #final_send_target = clean_number()
    send = '01020359827'
    
    send_message = '안녕하세요! 반갑습니다 \n 띄어쓰기가 되는지 모르겠습니다.'
    
    data = {
        'messages': [
            {
                'to': send,
                'from': SEND.SENDNUMBER,
                'subject': 'TEST',
                'text': send_message
             }
         ]
       }
    res = message.send_many(data)
    print(f"{send}에게 성공적으로 전송했습니다")
    print(json.dumps(json.loads(res.text), indent=2, ensure_ascii=False))
        
        
        
    