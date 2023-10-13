gnome.compile_resources('duplexer',
  'duplexer.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdata_dir,
)

configure_file(
  input: 'duplexer.in',
  output: 'duplexer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

subdir('backend')
subdir('frontend')
subdir('proto')

duplexer_sources = [
  '__init__.py',
  'main.py',
]

py_installation.install_sources(duplexer_sources, subdir: moduledir)
