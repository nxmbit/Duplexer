ipc_dir = join_paths(backend_dir, 'ipc')

configure_file(
  input: 'duplexer_dbus.xml.in',
  output: 'duplexer_dbus.xml',
  configuration: configuration_data({
    'APP_ID': APPLICATION_ID,

  }),
  install: true,
  install_dir: PY_INSTALLDIR.get_install_dir() / backenddir
)


ipc_sources = [
    '__init__.py',
    'ipc_handler.py',
    'socket_server.py',
    'dbus_service.py',
]

py_installation.install_sources(ipc_sources, subdir: ipc_dir)