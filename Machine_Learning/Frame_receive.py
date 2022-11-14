import socket
import struct
import pickle
import threading
import Recognition as rec
import cv2

class Cam(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name='Cam({})'.format(id))
        self.id = None
        self.frame = None
        self.data = {'cam_id': self.id, 'trash': False, 'intrusion': False, 'fallen': False,'restricted':False,'fence':False,'wall':False}
        self.url = "http://127.0.0.1:8000/home/change_stat"
        self.actrec = rec.actRecognition()
        self.e_list = []
        self.fxy_list = []
        self.txy_list = []
        self.trFrame_count = 0
        self.weight = 1

    def __repr__(self):
        return "CCTV_{}".format(self.id)

    def parse_data(self,data):
        """
        :param data: Received data from streaming process, decoded.
        :return: print id, restricted info
        """
        print("Parsing the CAM INFO...")
        self.id = int(data[data.find('cam_id') + 7:data.find('restricted') - 2])
        self.data['cam_id'] = self.id
        print("Cam_id: {}".format(self.id))
        if (data[data.find('restricted') + 11:data.find('wall') - 2]) == 'True':
            self.data['restricted'] = True
        else:
            self.data['restricted'] = False
        if (data[data.find('wall') + 5:]) == 'True':
            self.data['wall'] = True
        else:
            self.data['wall'] = False
        print("restricted: {}".format(self.data['restricted']))
        print("wall: {}".format(self.data['wall']))
        print(("COMPLETE"))

class Frame_recv():
    def __init__(self,HOST,PORT):
        self.host = HOST
        self.port = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None
        self.is_cam = False
        self.is_conn = True
        self.cam_no = None
        self.data = b""
        self.frame = None
        self.index = 0
        self.payload_size = struct.calcsize(">L")
        self.cam_list = ['cam0','cam1','cam2','cam3','cam4','cam5','cam6','cam7','cam8','cam9']
        self.f_number = [0,0,0,0,0,0,0,0,0,0]

    def __repr__(self):
        return 'Frame_recv'

    def conn_init(self):
        print('Socket bind complete')
        self.sock.bind((self.host,self.port))
        self.sock.listen(10)
        print('Socket now listening')
        self.conn, self.addr = self.sock.accept()
        self.is_cam = False

    def decode_data(self):
        data = self.conn.recv(1024)
        decoded = data.decode('utf-8')
        return decoded

    def make_cam(self): # 무한 루프문에서 돌게 하기
        decoded = self.decode_data()
        try:
            cam_num = int(decoded)  # Number of cameras
        except:
            self.is_cam = False
        else:  # Create objects for each camera
            self.conn.send("OK".encode("UTF-8"))
            print("Number of CCTV: {}".format(cam_num))
            for num in range(cam_num):
                decoded = self.decode_data()
                exec('{} =  Cam()'.format(self.cam_list[num]))
                exec("{}.parse_data(decoded)".format(self.cam_list[num]))
                exec("self.cam_list[num] = {}".format(self.cam_list[num]))

            self.cam_list = self.cam_list[:cam_num]
            self.is_cam = True

    def recv_frame(self):
        try:
            decoded = self.decode_data()
            self.conn.send(decoded.encode('utf-8'))
            self.index = int(decoded)
            # print("Cam({})'s Frame will be received".format(self.index))
            # Receive Frame SIZE from CCTV using TCP
            while len(self.data) < self.payload_size:
                self.data += self.conn.recv(4096)
        except ConnectionResetError:
            print("ConnectionResetError")
            self.conn.close()
            self.is_conn = False
        except ValueError:
            print("ValueError")
            self.conn.close()
            self.is_conn = False
        else:
            packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            # print("msg_size: {}".format(msg_size))
            while len(self.data) < msg_size:
                self.data += self.conn.recv(4096)
            frame_data = self.data[:msg_size]
            self.data = self.data[msg_size:]
            # Decode encoded Frame
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            self.frame = frame
            self.cam_list[self.index].weight = 1

    def send_weight(self,index):
        self.conn.send(str(self.cam_list[index].weight).encode("UTF-8"))

    def run(self):
        if not self.is_cam:
            self.make_cam()
        self.recv_frame()
        self.cam_list[self.index].frame = self.frame
        return self.index

    def capture(self, camid):
        # png로 압축 없이 영상 저장
        name = '/img_{}.png'.format(self.f_number[camid])
        self.f_number[camid] += 1
        cv2.imwrite(
            'C:/Users/Jun-Young/Desktop/EDUM/ICE_CAP/Django_channels/mysite/notifier/statics/' + str(camid) + name,
            self.cam_list[self.index].frame, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
        if self.f_number[camid] == 3:
            self.f_number[camid] = 0