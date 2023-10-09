import json
import os
import cups
import logging
import tempfile
import keyboard

logger = logging.getLogger(__name__)


class Printer:
    def __init__(self, printer_name, virtual_name, connection):
        self.printer_name = printer_name
        self.virtual_name = virtual_name
        self.connection = connection
        self.uri = self.get_uri()

    @classmethod
    def from_json(cls, json_path, virtual_name, conn):
        with open(json_path, "r") as file:
            printers_json = json.load(file)
            try:
                printer_data = printers_json[virtual_name]
            except KeyError:
                logger.error(f"Printer {virtual_name} not found in {json_path}")
                raise
            except FileNotFoundError:
                logger.error(f"Could not find file {json_path}")
                raise
            return cls(connection=conn, **printer_data)

    @staticmethod
    def is_virtual(printer_name):
        pass

    def to_json(self, json_path):
        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                printer_data = json.load(file)
        else:
            printer_data = {}

        printer_data[self.virtual_name] = {
            "printer_name": self.printer_name,
            "virtual_name": self.virtual_name,
        }

        with open(json_path, "w") as file:
            json.dump(printer_data, file)

    def get_printer_info(self):
        return self.connection.getPrinterAttributes(self.printer_name)

    def get_supported_mime_types(self):
        ppd = self.get_ppd()
        types = []
        for line in ppd:
            if line.startswith("*cupsFilter"):
                types.append(line.split(" ")[1])
        return types

    def get_ppd(self):
        ppd_path = self.connection.getPPD(self.printer_name)
        try:
            with open(ppd_path, "r") as file:
                ppd = file.readlines()
        except FileNotFoundError:
            logger.error(f"Could not find PPD file at {ppd_path}")
            raise

        return ppd

    def get_status(self):
        printer_state = self.get_printer_info()["printer-state"]

        if printer_state == cups.IPP_PRINTER_IDLE:
            return "idle"
        elif printer_state == cups.IPP_PRINTER_PROCESSING:
            return "processing"
        elif printer_state == cups.IPP_PRINTER_BUSY:
            return "busy"
        elif printer_state == cups.IPP_PRINTER_STOPPED:
            return "stopped"
        elif printer_state == cups.IPP_PRINTER_IS_DEACTIVATED:
            return "deactivated"

    def get_uri(self):
        printer_info = self.get_printer_info()
        return printer_info["device-uri"]

    def save_temp_file(self, file):
        try:
            with tempfile.NamedTemporaryFile(mode="wb", prefix="duplexer_", delete=False) as temp_file:
                temp_file.write(file)
                return temp_file.name
        except PermissionError:
            logger.error(f"Could not write file to temporary directory - permission denied")
            raise

    def print_from_file(self, file_path, title, options=None):
        if options is None:
            options = {}

        job_id = self.connection.printFile(self.printer_name, file_path, title, options)
        return job_id

    def print_from_memory(self, file, title, options=None):
        if options is None:  # do this instead of options = {} in the function definition (mutable default argument)
            options = {}

        job_id = self.connection.createJob(self.printer_name, title, options)
        self.connection.startDocument(self.printer_name, job_id, title, cups.CUPS_FORMAT_POSTSCRIPT, True)
        self.connection.writeRequestData(file, len(file))
        self.connection.finishDocument(self.printer_name)
        logger.debug(f"Sent document '{title}' to printer '{self.printer_name}' with job ID: {job_id}")

    @staticmethod
    def prompt_first_side():
        print("Make sure that there is paper in the printer, then press Enter to print the first side")
        keyboard.wait("enter")

    @staticmethod
    def prompt_second_side():
        print("Flip the paper and press Enter to print the second side")
        keyboard.wait("enter")

    def print_duplex(self, file, title, options):
        tmp_file_path = self.save_temp_file(file)

        self.prompt_first_side()
        options["page-set"] = "odd"
        self.print_from_file(tmp_file_path, title, options)

        self.prompt_second_side()
        options["page-set"] = "even"
        self.print_from_file(tmp_file_path, title, options)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.printer_name}', {self.connection})"
