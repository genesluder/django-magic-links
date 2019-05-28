from distutils.core import setup
setup(
  name = 'django-magic-links',
  packages = [
    'magic_links',
    'magic_links/migrations',
    'magic_links/urls',
    'magic_links/views',
  ],
  version = '0.1.0',
  description = '',
  author = 'Gene Sluder',
  author_email = 'gene@gobiko.com',
  url = 'https://github.com/genesluder/django-magic-links',
  download_url = 'https://github.com/genesluder/django-magic-links/tarball/0.1.0',
  keywords = [
  ],
  classifiers = [],
  install_requires=[
    'bcrypt',
    'django-rest-framework',
  ],
)
