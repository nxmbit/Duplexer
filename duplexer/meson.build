pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'duplexer')

gnome.compile_resources('duplexer',
  'duplexer.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

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
