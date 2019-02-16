from app.mod_publisher.zmqpublisher import publisher,conf
import threading
from  app.block.block import Block

def test():


        bblock = Block(5,5,5,5,5)

        pub = publisher('182.48.107.140', '1234', 'new_block')
        # pub.publish_newblock(block)
        _pub_thread = threading.Thread(target=pub.publish_newblock, kwargs={'data': bblock})
        _pub_thread.start()

        _status = publisher(conf['private_server'], conf['signal_port'], '')
        _status_thread = threading.Thread(target=_status.req_rep)
        _status_thread.start()

test();