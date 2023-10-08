#!/bin/bash

sudo cp -rf duplexer_filter /usr/lib/cups/filter/duplexer_filter
sudo cp -rfL duplexer_ipc_pb2.py /usr/lib/cups/filter/duplexer_ipc_pb2.py
sudo chown root:root /usr/lib/cups/filter/duplexer_filter
sudo chown root:root /usr/lib/cups/filter/duplexer_ipc_pb2.py
sudo chmod 755 /usr/lib/cups/filter/duplexer_filter
sudo chmod 755 /usr/lib/cups/filter/duplexer_ipc_pb2.py
sudo restorecon -vFr /usr/lib/cups/filter/duplexer_filter
sudo restorecon -vFr /usr/lib/cups/filter/duplexer_ipc_pb2.py

sudo cp -rf duplexer /usr/lib/cups/backend/duplexer
sudo chown root:root /usr/lib/cups/backend/duplexer
sudo chmod 755 /usr/lib/cups/backend/duplexer
sudo restorecon -vFr /usr/lib/cups/backend/duplexer