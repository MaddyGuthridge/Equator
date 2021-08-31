from setuptools import setup

DESCRIPTION = 'An advanced symbolic calculator'
LONG_DESCRIPTION = 'This .'

setup(
    name='EquatorPy',
    version='1.1.0',
    author="Miguel Guthridge",
    author_email="hdsq@outlook.com.au",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=['equator'],
    install_requires=[
        'sympy',
        'colorama',
        "windows-curses >= 2.2.0;platform_system=='Windows'"
    ],
    keywords=['equator', 'calculator', 'symbolic', 'math', 'equation', 'sympy'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={
    'Documentation': 'https://github.com/MiguelGuthridge/Equator/wiki',
    'Source': 'https://github.com/MiguelGuthridge/Equator',
    'Tracker': 'https://github.com/MiguelGuthridge/Equator/issues',
    },
)
