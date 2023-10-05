#!/usr/bin/python
import cups
import os
import sys
import logging

import constants
from printer_manager import PrinterManager
from cli import Cli

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=constants.LOG_PATH, filemode="w")

os.environ["GDK_BACKEND"] = "x11"
os.environ["DISPLAY"] = ":0"

def main():
    connection = cups.Connection()
    cli = Cli(connection)
    Gtk.init()
    cli.cli()

if __name__ == "__main__":
    main()


# manager = PrinterManager()
# print(manager.get_printers())
# manager.install_printer("DCPJ105")
# manager.modify_ppd("DCPJ105")
# print(manager.installed_printers)
# print(manager.installed_printers[0].get_printer_info())
# print(manager.installed_printers[0].get_ppd_path())
# print(manager.installed_printers[0].get_uri())
