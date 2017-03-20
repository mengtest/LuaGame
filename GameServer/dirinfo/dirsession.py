# -*- coding: utf-8 -*-
import os

from network.server import TCPConnectionDelegage
from utils.logger import logger
from protobuf import pb_helper
from protobuf import message_common_pb2

class DirSession(TCPConnectionDelegage):
    def __init__(self):
        TCPConnectionDelegage.__init__(self)
    def on_receive(self, data):
        logger().i("receive from %s, %s", str(self.address),pb_helper.debug_bytes(data))
        msg = pb_helper.BytesToMessage(data)
        if isinstance(msg, message_common_pb2.DirInfo):
            self._send_dirinfo()
        else:
            self.close()
    def _send_dirinfo(self):
        path = os.path.split(os.path.realpath(__file__))[0].replace("\\", "/")
        filename = path + "/bin/version.xml"
        msg = message_common_pb2.DirInfo()
        with open(filename,"rb") as fin:
            data = fin.read()
            msg.version = data
            fin.close()
        buff = pb_helper.MessageToSendBytes(msg)
        logger().i("send dirinfo to %s, %s", str(self.address), pb_helper.debug_bytes(buff))
        self.send(buff)
    def on_write_complete(self):
        #self.close()
        pass