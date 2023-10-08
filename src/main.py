#!/usr/bin/python
import cups
import os
import sys
import logging

from duplexer.backend.cli import Cli
from duplexer.backend import constants

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=constants.LOG_PATH, filemode="w")

os.environ["GDK_BACKEND"] = "x11"
os.environ["DISPLAY"] = ":0"

def main(version):
    connection = cups.Connection()
    cli = Cli(connection)
    Gtk.init()
    cli.cli()

if __name__ == "__main__":
    main()

