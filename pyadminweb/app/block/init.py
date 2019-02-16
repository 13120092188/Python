from app.block.block import Block
import datetime as date
def create_genesis_block():
    # Manually construct a bbb with
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), "Genesis Block", "0",5)