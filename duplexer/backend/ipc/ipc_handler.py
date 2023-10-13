import cups
import logging

from duplexer.backend import xdg_globals
from duplexer.proto import duplexer_ipc_pb2
from duplexer.backend.printer import Printer
from duplexer.backend import constants

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=xdg_globals.duplexer_log_path, filemode="w")


class IPCHandler:
    def __init__(self, recv_data):
        self.recv_data = recv_data
        self.connection = cups.Connection()

        data = duplexer_ipc_pb2.PrintRequest()
        data.ParseFromString(self.recv_data)

        options = data.options.split(" ")
        options_dict = {}
        for option in options:
            if "=" in option:
                key, value = option.split("=")
                options_dict[key] = value

        self.args = {
            "virtual_printer": data.virtual_printer,
            "job_id": data.job_id,
            "user": data.user,
            "title": data.title,
            "num_copies": data.num_copies,
            "options": options_dict
        }
        self.file = data.file

    def print(self):
        logger.info("Filter called")
        logger.info(f"args: {self.args}")

        printer = Printer.from_json(xdg_globals.duplexer_virtual_printers_path, self.args["virtual_printer"], self.connection)
        logger.debug(printer.get_status())
        printer.print_duplex(self.file, self.args["title"], self.args["options"])
