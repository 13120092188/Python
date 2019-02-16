import time
import zmq
import json
import os
import threading


#Server是消息队列的地址，
#Private_server是消息队列的内部地址（对阿里云的私有网络配置，如果是其他网络，两者可以是同一个地址）
#Port是端口号
#Sub_topic客户端的订阅主题
#Pre_file数据文件的前缀
#Signal_port接收计算完成信号的端口
#Write_port接收分布式数据的端口

_basepath = os.path.abspath(os.path.dirname(__file__))
conf = json.load(open(os.path.abspath(os.path.dirname(__file__))+"\\conf.json"))

class publisher:
    def __init__(self, bindserver,port,pub_key,pub_data=''):
        self.server = bindserver
        self.port = port
        #self.timestamp = timestamp
        self.key = pub_key
        self.data = pub_data
#发布新区块计算方法
    def publish_newblock(self,**block):
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        publisher.bind("tcp://*:1234")

        block_string = json.dumps(block['data'].__dict__, sort_keys=True)

        i = 0
        while True:
            publisher.send_multipart([b'new_block', bytes(block_string,'utf-8')])
            time.sleep(2)
            print(i)
            i+=1
            if i==2:
                break

        publisher.close()
        context.term()


    def publish_write_newblock(self,block):
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        publisher.bind("tcp://*:1234")

        block_string = json.dumps(block, sort_keys=True)

        i = 0
        while True:
            publisher.send_multipart([b'write_block', bytes(block_string,'utf-8')])
            time.sleep(2)
            print(i)
            i+=1
            if i==2:
                break

        publisher.close()
        context.term()

    def req_rep(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:1234")

        while True:
            #  Wait for next request from client
            data = socket.recv()
            data_str = data.decode(encoding="utf-8")

            return data_str

            if  'finished' in data_str:
                #time.sleep(10)
                data_obc = json.loads(data_str)

                pub_write = publisher(conf["private_server"],conf["write_port"],'')

                pub_write.publish_write_newblock(data_obc['finished'])
                socket.close()
                context.term()
                break




