# Create the blockchain and add the genesis bbb
from app.block.next import *
from app.block.init import *
import json

dict=[]
with open("app/block/record.json", "w") as f:
    f.write(json.dumps(dict, ensure_ascii=False, indent=2))

blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# How many blocks should we add to the chain
# after the genesis bbb
num_of_blocks_to_add = 40
diff=0

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
    if (i % 5 == 0 and i != 0):
        diff = Adjust_of_diff(diff)
    print(diff)
    data="    "
    block_to_add = next_block(previous_block,diff,data)
    previous_block = block_to_add
    # Tell everyone about it!
    #print("Block #{} has been added to the blockchain!".format(block_to_add.index))
    #print("Hash: {}\n".format(block_to_add.hash))


# with open("../record.json", "r") as k:
#     new_dict=json.load(k)
    # print (new_dict[1]['data'])