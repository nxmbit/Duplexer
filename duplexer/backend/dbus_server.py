import logging
from gi.repository import Gio, GLib

from duplexer.backend import xdg_globals
from duplexer.proto import duplexer_ipc_pb2
from duplexer.backend.printer import Printer
from duplexer.backend import constants

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=xdg_globals.duplexer_log_path, filemode="w")




