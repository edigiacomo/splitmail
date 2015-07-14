from setuptools import setup


setup(
    name='splitmailbox',
    version='0.0.0',
    description='Simple tool to split your mailbox',
    license='GPLv2+',
    author='Emanuele Di Giacomo',
    author_email='emanuele.digiacomo@gmail.com',
    url='https://github.com/edigiacomo/splitmailbox',
    packages=['splitmailbox'],
    entry_points={
        'console_scripts': [
            'splitmailbox=splitmailbox:main',
        ],
    },
)
