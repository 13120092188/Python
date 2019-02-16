import zmq
import threading
import json
from hashlib import sha256
import os
import time

#182.48.107.148

_basepath = os.path.abspath(os.path.dirname(__file__))
conf = json.load(open(os.path.abspath(os.path.dirname(__file__))+"\\conf.json"))
hash=0
class subscriber:
    def __init__(self, bindserver,port,pub_key):
        self.server = bindserver
        self.port = port
        self.key = pub_key

    #sub new block event
    def sub_newblock(self):
        # Prepare our context and subscriber
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://localhost:1234")
        subscriber.setsockopt(zmq.SUBSCRIBE, bytes(self.key,'utf-8'))


        while True:
            # Read envelope with address
            [address, contents] = subscriber.recv_multipart()
            print("[%s] %s" % (address, contents))
            compute_hash(contents)

        subscriber.close()
        context.term()

    #sub write event
    def write_newblock(self):
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://localhost:1234")
        subscriber.setsockopt(zmq.SUBSCRIBE, bytes(self.key, 'utf-8'))

        while True:
            # Read envelope with address
            [address, contents] = subscriber.recv_multipart()
            print("[%s] %s" % (address, contents))
            write_blockfile(contents)

        subscriber.close()
        context.term()


def compute_hash(data):
    """
    A function that return the hash of the block contents.
    """
    #block_string = self.transactions+str(self.nonce)
    global hash
    a=0
    block_object = json.loads(data)
    computed_hash = sha256(str(data,'utf-8').encode()).hexdigest()
    while not computed_hash.startswith('0' * 5):

        block_object['nonce'] +=1
        ee = json.dumps(block_object)
        if(a==0):
            computed_hash = sha256(ee.encode()).hexdigest()
            hash=computed_hash
            print(computed_hash)
            print("计算hash成功")
            a=a+1

        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:1234")
        socket.send(bytes(str(computed_hash), 'utf-8'))

    print('最终结果是:{}, 随机数:{}'.format(computed_hash, block_object['nonce']))

    #send signal of status,FIFO
    #time.sleep(10)
    #send_finish_status(block_object)


    return computed_hash


# send signal
def send_finish_status(block_object):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://*:1234")
    print('fdsfffffffffffffff===',type(block_object),block_object)
    block_dict = {}
    block_dict['finished'] = block_object
    block_string = json.dumps(block_dict)
    socket.send(bytes(block_string,'utf-8'))

def write_blockfile(data):
    obj_data = json.loads(data.decode(encoding="utf-8"))
    #print('the file ==================',obj_data," and index is ",json.dumps(obj_data,indent=2,ensure_ascii=False))
    with open(_basepath+'/block'+str(obj_data['index'])+'.txt', 'w',encoding="utf-8") as f:
        f.write(json.dumps(obj_data,indent=2,ensure_ascii=False))

print('消息服务器',conf["server"])
_newblock_sub = subscriber(conf["server"],conf["port"],conf["sub_topic"])
#instead of s.sub_newblock(),we use thread fun,avoid locking
_newblock_thread = threading.Thread(target=_newblock_sub.sub_newblock)
_newblock_thread.start()


_writeblock_sub = subscriber(conf["server"],conf["write_port"],"write_block")
_writeblock_thread = threading.Thread(target=_writeblock_sub.write_newblock)
_writeblock_thread.start()
