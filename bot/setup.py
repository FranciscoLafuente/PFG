
from setuptools import setup, find_packages
from bot.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='bot',
    version=VERSION,
    description='Bot que obtiene el banner grabing de una ip dada',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Fran Lafuente',
    author_email='pacolafuente_5@hotmail.com',
    url='-',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'bot': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        bot = bot.main:main
    """,
)
