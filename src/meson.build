pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'twitz')
gnome = import('gnome')

gnome.compile_resources('twitz',
  'twitz.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'twitz.in',
  output: 'twitz',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

twitz_sources = [
  '__init__.py',
  'about.py',
  'main.py',
  'window.py',
  'chat.py',
  'globals.py',
  'player.py',
  'login.py',
  'preferences.py',
]

install_data(twitz_sources, install_dir: moduledir)
