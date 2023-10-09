project('duplexer',
          version: '0.1.0',
    meson_version: '>= 0.62.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

dependency('glib-2.0')
dependency('gtk4', version: '>= 4.5.0')
dependency('libadwaita-1', version: '>= 1.3.99')

python = import('python')
i18n = import('i18n')
gnome = import('gnome')

pkgdata_dir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
module_dir = join_paths(pkgdata_dir, 'duplexer')

py_installation = python.find_installation('python3', required: true)

if not py_installation.found()
    error('No python3 installation found')
endif

conf = configuration_data()
conf.set('PKGDATA_DIR', pkgdata_dir)
conf.set('DATA_DIR', join_paths(get_option('prefix'), get_option('datadir')))
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('localedir')))

subdir('data')
subdir('duplexer')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
