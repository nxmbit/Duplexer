import cups
import logging

from duplexer.backend import xdg_globals
from duplexer.backend.printer import Printer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=xdg_globals.duplexer_log_path, filemode="w")

