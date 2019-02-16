from app import app
from app.block.next import *
from app.block.init import *
import json
dict=[]
with open("app/block/record.json", "w") as f:
    f.write(json.dumps(dict, ensure_ascii=False, indent=2))

blockchain=[create_genesis_block()]
app.run(host='127.0.0.1', debug=False, port=5000)