from app.block.block import *
import datetime as date
def next_block(last_index,last_hash,d,data):
    this_index = last_index + 1
    this_timestamp = date.datetime.now()
    this_data = data
    this_hash = last_hash
    this_diff=d
    return Block(this_index, this_timestamp, this_data, this_hash,this_diff)


def Adjust_of_diff(d):
    filer = open('app/block/record.json', 'r', encoding='utf-8')
    # record = json.load(filer)
    dic = eval(filer.read())
    filer.close()
    starttime = dic[len(dic) - 5][str(len(dic) - 5)]['timestamp']
    endtime = dic[len(dic) - 1][str(len(dic) - 1)]['timestamp']
    t1 = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S.%f")
    t2 = datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S.%f")
    print(t2 - t1)
    if (str(t2 - t1) < '0:00:10.000000'):
      return d + 1
    else:
      return d - 1
