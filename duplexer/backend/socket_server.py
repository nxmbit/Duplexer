import socket
import os
#import daemon
import errno
import logging
import cups
import struct
from duplexer.backend import constants
from duplexer.backend import xdg_globals
from duplexer.backend.ipc_handler import IPCHandler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=xdg_globals.duplexer_log_path, filemode="w")


class Daemon:
    def __init__(self, socket_path):
        self.socket_path = socket_path
        self.connection = cups.Connection()
        self.is_running = False

    def socket_server(self):
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.bind(self.socket_path)
        except PermissionError:
            logger.info(f"Permission denied when binding to socket at {self.socket_path}")
            raise
        except FileNotFoundError:
            logger.info(f"Could not find socket at {self.socket_path}")
            raise
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                logger.info(f"Socket at {self.socket_path} is already in use")
                raise
        os.chmod(self.socket_path, 0o777)
        sock.listen(1)

        while self.is_running:
            logger.info("Waiting for connection")
            conn, addr = sock.accept()
            data_size = struct.unpack("!I", conn.recv(4))[0]
            data = conn.recv(data_size)

            if data:
                logger.info(f"Received data of size: {len(data)}") #TODO: display data size properly
                handler = IPCHandler(data)
                handler.print()

    def run(self):
        self.is_running = True
        self.socket_server()
        #with daemon.DaemonContext():
        #    self.socket_server()

