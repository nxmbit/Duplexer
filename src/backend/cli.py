import argparse
import sys
import logging
import keyboard
from duplexer.backend.printer_manager import PrinterManager
from duplexer.backend.ipc_server import Daemon
from duplexer.backend import constants

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=constants.LOG_PATH, filemode="w")


class Cli:
    def __init__(self, conn):
        self.connection = conn

    def get_parser(self):
        parser = argparse.ArgumentParser(description="An application for manual duplex printing",
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        subparsers = parser.add_subparsers(dest="subcommand")

        manager_subparser = subparsers.add_parser("manager", help="manage installed printers")
        list_printers = manager_subparser.add_mutually_exclusive_group()
        list_printers.add_argument("--list_printers", "-l", action="store_true", help="list all printers")
        list_printers.add_argument("--list_installed", action="store_true", help="list installed printers")
        list_printers.add_argument("--list_available", action="store_true", help="list available printers")
        installer = manager_subparser.add_mutually_exclusive_group()
        installer.add_argument("--install", "-i", type=str, metavar="[printer name]",
                               help="install virtual printer for specified printer")
        installer.add_argument("--remove", "-r", type=str, metavar="[printer name]",
                               help="remove virtual printer for specified printer")

        daemon_subparser = subparsers.add_parser("daemon")
        daemon_subparser.add_argument("--run", "-r", action="store_true", help="start daemon")
        daemon_subparser.add_argument("--stop", "-s", action="store_true", help="stop daemon")
        daemon_subparser.add_argument("--status", action="store_true", help="check daemon status")

        return parser

    def manager(self, args):
        logger.debug("Manager called")
        logger.debug(f"args: {args}")

        manager = PrinterManager.from_json(constants.JSON_FILENAME)

        if args.list_printers:
            for printer in manager.get_printers_list():
                pass

        elif args.list_installed:
            print(manager.installed_printers)
        elif args.list_available:
            print(manager.get_printers_list()) #TODO: filter out installed printers

        if args.install:
            print(f"Installing virtual printer for {args.install}")
            manager.install_virtual_printer(args.install)
        elif args.remove:
            print(f"Removing virtual printer for {args.remove}")
            manager.remove_virtual_printer(args.remove)

    def daemon(self, args):
        dmon = Daemon(constants.SOCKET_PATH)
        if args.run:
            dmon.run()
        elif args.stop:
            pass
        elif args.status:
            pass


    def cli(self):
        # app = MyApp(application_id="com.example.GtkApplication")
        # app.run()
        parser = self.get_parser()
        args = parser.parse_args()

        if args.subcommand == "manager":
            self.manager(args)
        elif args.subcommand == "daemon":
            self.daemon(args)
        elif not args.subcommand:
            parser.print_help()
        # if not vars(args):
        #    self.get_parser().print_help()
