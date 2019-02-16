import hashlib as hasher
import json
import pymysql
import time
import datetime
class Block:
    def __init__(self, index, timestamp, data, previous_hash,diff):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.proof_of_work(self,diff)

        filer = open('app\\block\\record.json', 'r', encoding='utf-8')
        record = json.load(filer)
        filer.close()
        #print(record)

        dict={index:{
              'index':index,
              'timestamp':str(timestamp),
              'data':data,
              'previous_hash':previous_hash,
              'self.hash':self.hash,
              'nonce':self.nonce,
              'diff':diff
        }
        }
        conn = pymysql.connect(host='127.0.0.1', user='root', password='loveyangxun.MY', db='flask', charset="utf8")
        sql = "insert into json(numIndex, timestamp, data, pre_hash, self_hash, nonce, diff) " \
              "values('%s','%s','%s','%s','%s','%s','%s')" % (
            index, str(timestamp), data, previous_hash, self.hash, self.nonce, diff)
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()

        cursor.close()

        l = []
        if record != None:#########################
            for i in record:
                l.append(i)
        l.append(dict)

        with open("app/block/record.json", "w") as f:
            # json.dump(dict,f)
            f.write(json.dumps(l, ensure_ascii=False, indent=2))
        #print(self.timestamp)

    def hash_block(self):
        sha = hasher.sha256()
        #while(sha.hexdigest()> '000000''ffffffffff''ffffffffff'
         #                      'ffffffffff''ffffffffff''ffffffffff''fffffffff'):
        sha.update((str(self.index) +
                   str(self.timestamp) +
                   str(self.data) +
                   str(self.nonce)+str(self.previous_hash)).encode("utf8"))
            #self.index+=1
        return sha.hexdigest()

    def proof_of_work(self,block,diff):
        block.nonce = 0
        block.hash=block.hash_block()
        while not block.hash.startswith('0' * diff):
            block.nonce += 1
            block.hash=block.hash_block()
            #print(block.hash)
        #print('最终结果是:{}, 随机数:{}'.format(block.hash, block.nonce))
        return block.hash







