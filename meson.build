project('duplexer',
          version: '0.1.0',
    meson_version: '>= 0.62.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

# Project information constants
PROJECT_URL = 'https://github.com/nxmbit/Duplexer'
PROJECT_RDNN_NAME = 'com.github.nxmbit.duplexer'

if get_option('buildtype') == 'debug'
  git_bin = find_program('git', required: false)
  if git_bin.found()
    VCS_TAG = run_command('git', 'rev-parse', '--short', 'HEAD', check: true).stdout().strip()
  else
    VCS_TAG = ''
  endif
  if VCS_TAG == ''
    VERSION_SUFFIX = '-devel'
  else
    VERSION_SUFFIX = '-@0@'.format(VCS_TAG)
  endif
  APPLICATION_ID = '@0@.Devel'.format(PROJECT_RDNN_NAME)
else
  VERSION_SUFFIX = ''
  APPLICATION_ID = PROJECT_RDNN_NAME
endif


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
conf.set('APP_ID', APPLICATION_ID)
conf.set('PKGDATA_DIR', pkgdata_dir)
conf.set('DATA_DIR', join_paths(get_option('prefix'), get_option('datadir')))
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('PYTHON', py_installation.full_path())
conf.set('VERSION', meson.project_version() + VERSION_SUFFIX)


subdir('data')
subdir('duplexer')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
