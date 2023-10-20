import logging
from gi.repository import Gio, GLib

from duplexer.backend import xdg_globals
from duplexer.backend.printer import Printer
from duplexer.backend import constants

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=xdg_globals.duplexer_log_path, filemode="w")


class DBusService():
    def __init__(self, bus_conn: Gio.DBusConnection, object_path: str, xml: str):
        for interface in Gio.DBusNodeInfo.new_for_xml(xml).interfaces:
            bus_conn.register_object(object_path, interface, self.method_call_handler)

    def method_call_handler(self, bus_conn: Gio.DBusConnection, sender: str, object_path: str,
                            interface_name: str, method_name: str, parameters: GLib.Variant,
                            invocation: Gio.DBusMethodInvocation):
        logger.debug(f"Received method call: {method_name}")


class DuplexerService(DBusService):
    def __init__(self):
        pass

    def _get_xml(self):
        xml = f"""
        <!DOCTYPE node PUBLIC 
        "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
        "http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">
        <node>
            <interface name="org.duplexer.Duplexer">
                <method name="GetPrintingArgs">
                <arg direction="in" name=job_id" type="i"/>
                <arg direction="in" name="user" type="s"/>
                <arg direction="in" name="title" type="s"/>
                <arg direction="in" name="num_copies" type="i"/>
                <arg direction="in" name="options" type="s"/>
                <arg direction="in" name="virtual_printer" type="s"/>
                <arg direction="out" name="response" type="b"/>
                </method>
                <method name="GetFile">
                <arg direction="in" name="file" type="ay"/>
                <arg direction="out" name="response" type="b"/>
                </method>
            </interface>
        </node>        
        """
        return xml

    def GetPrintingArgs(self, job_id: int, user: str, title: str,
                        num_copies: int, options: str, virtual_printer: str) -> bool:

        logger.debug(f"job_id: {job_id}")
        logger.debug(f"user: {user}")
        logger.debug(f"title: {title}")
        logger.debug(f"num_copies: {num_copies}")
        logger.debug(f"options: {options}")
        logger.debug(f"virtual_printer: {virtual_printer}")

        options_dict = {}
        for option in options.split(" "):
            if "=" in option:
                key, value = option.split("=")
                options_dict[key] = value

        self.args = {
            "virtual_printer": virtual_printer,
            "job_id": job_id,
            "user": user,
            "title": title,
            "num_copies": num_copies,
            "options": options_dict
        }

        return True
