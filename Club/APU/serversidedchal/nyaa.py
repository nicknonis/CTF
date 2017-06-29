#!python3

import sys
import socket
import threading

"""The flag is FLAG_フラッグはここだよ"""

questions = [
    b"%65%7A%70%7A%5F%6C%65%6D%6F%6E%5F%73%71%75%65%65%7A%79", #1 URL Encode
    b"d2hhdGRhZnVxaXN0aGlzPw==", #2 Base64
    b"qnza_v_unirag_qbar_zl_nffvtazragf", #3 ROT13
    b"9O4phLqskR3xWB4E+", #4 Xxencode
    b"OR3WS3TLNRSV65DXNFXGW3DFL5WGS5DUNRSV643UMFZA=====", #5 Base32
]
answers = [
    b"ezpz_lemon_squeezy", #1
    b"whatdafuqisthis?", #2
    b"damn_i_havent_done_my_assignments", #3
    b"hmm_n0t_b4d", #4
    b"twinkle_twinkle_little_star", #5
]

class ClientThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.conn = client[0]
        self.addr = client[1]
        self.progress = 0
    
    def run(self):
        try:
            while True:
                self.conn.send(b"\nLevel " + bytes(str(self.progress + 1), 'utf-8') +
                               b"\n" + questions[self.progress] +
                               b"\nAnswer:")
                data = self.conn.recv(1024)
                if not data: break
                print("{}:{} - {}".format(self.addr[0],self.addr[1],str(data[:-1])))
                if data[:-1] == answers[self.progress]:
                    self.progress += 1
                    if self.progress == len(questions):
                        self.conn.send(b"\nCongratulations, the flag is \n0046004C00410047005F30D530E930C330B0306F3053305330603088\n\nHmm, maybe not.\n\n")
                        break
                else:
                    self.conn.send(b"WRONG!\n")
            self.conn.close()
        except:
            print("Error: " + str(sys.exc_info()[0]))
            print("Closing connection: {}:{}".format(self.addr[0],self.addr[1]))
            self.conn.send(b'Connection closed');
            self.conn.close()
        

if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 10000))
        s.listen(5)
        print("Server started at port 10000")
        
        threads = []
        while True:
            c = ClientThread(s.accept())
            c.start()
            threads.append(c)
    except:
        print("Error: " + str(sys.exc_info()[0]))
        print("Exiting")
        exit()
        
    
    