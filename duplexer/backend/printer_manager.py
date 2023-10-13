import cups
import json
import os
import logging
import tempfile

from duplexer.backend import xdg_globals
from duplexer.backend import constants
from duplexer.backend.printer import Printer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=xdg_globals.duplexer_log_path, filemode="w")


class PrinterManager:
    def __init__(self):
        self.manager_conn = cups.Connection()
        self.filter_is_installed = False
        self.installed_printers = []

    @classmethod
    def from_json(cls, json_path):
        manager = cls()

        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                printers_json = json.load(file)

            for virtual_name in printers_json:
                printer = Printer.from_json(json_path, virtual_name,
                                            manager.manager_conn)  # TODO: do not open json multiple times
                manager.installed_printers.append(printer)

        return manager

    def get_printers_list(self):
        printers = self.manager_conn.getPrinters()
        return list(printers.keys())

    def install_virtual_printer(self, printer_name):
        virtual_printer_name = printer_name + "_Duplexer"
        printer = Printer(printer_name, virtual_printer_name, self.manager_conn)
        filename = self.modify_ppd(printer_name)
        info = "Duplexer virtual printer for " + printer_name
        uri = constants.BACKEND_FILENAME + ":" + virtual_printer_name
        # uri = printer.get_uri()
        location = printer.get_printer_info()["printer-location"]

        self.manager_conn.addPrinter(name=virtual_printer_name, filename=filename,
                                    info=info, device=uri, location=location)
        self.manager_conn.enablePrinter(virtual_printer_name)
        self.manager_conn.acceptJobs(virtual_printer_name)

        printer.to_json(xdg_globals.duplexer_virtual_printers_path)
        self.installed_printers.append(printer)
        logger.info(f"Installed virtual printer for {printer_name}")

    def remove_virtual_printer(self, virtual_printer_name):
        try:
            with open(xdg_globals.duplexer_virtual_printers_path, "r") as file:
                printers_json = json.load(file)
            try:
                printers_json.pop(virtual_printer_name)
            except KeyError:
                logger.error(f"Printer {virtual_printer_name} not found in {xdg_globals.duplexer_virtual_printers_path}")
                raise
            try:
                with open(xdg_globals.duplexer_virtual_printers_path, "w") as file:
                    json.dump(printers_json, file)
            except PermissionError:
                logger.error(f"Could not write to file {xdg_globals.duplexer_virtual_printers_path} - permission denied")
                raise
            self.manager_conn.deletePrinter(virtual_printer_name)
            logger.info(f"Removed virtual printer: {virtual_printer_name}")
        except FileNotFoundError:
            logger.error(f"Could not find file {xdg_globals.duplexer_virtual_printers_path}")
            raise
        except PermissionError:
            logger.error(f"Could not read file {xdg_globals.duplexer_virtual_printers_path} - permission denied")
            raise

    def modify_ppd(self, printer_name):
        ppd_path = self.manager_conn.getPPD(printer_name)
        try:
            with open(ppd_path, "r") as file:
                ppd = file.readlines()
        except FileNotFoundError:
            logger.error(f"Could not find PPD file at {ppd_path}")
            raise

        new_ppd = []
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=('_' + printer_name + '_' + "duplexer.ppd"),
                                             prefix=printer_name, delete=False) as temp_file:
                is_cupsfilter = False
                for line in ppd:
                    if line.startswith("*cupsFilter:") or line.startswith("*cupsFilter2:"):
                        is_cupsfilter = True
                        split_line = line.split(" ")
                        split_line[-1] = f"{constants.FILTER_FILENAME}\"\n"
                        line = " ".join(split_line)
                    new_ppd.append(line)

                if not is_cupsfilter:
                    new_ppd.append(f"*cupsFilter: \"application/vnd.cups-postscript 0 {constants.FILTER_FILENAME}\"\n")
                    new_ppd.append(f"*cupsFilter: \"application/vnd.cups-pdf 0 {constants.FILTER_FILENAME}\"\n")

                temp_file.writelines(new_ppd)
                logger.debug(f"Created temporary file: {temp_file.name}")
                return temp_file.name
        except PermissionError:
            logger.error(f"Could not write file to temporary directory - permission denied")
            raise
