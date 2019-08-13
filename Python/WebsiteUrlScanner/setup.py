from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = r'C:\Users\jason.brown\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\jason.brown\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'

# Dependencies are automatically detected, but some modules need help.
buildOptions = dict(
    packages = [ 'bs4', 'sys', 'Wappalyzer','csv','whois','os','lxml','six','appdirs','pkg_resources','idna','argparse' ],
    include_files=['Wappalyzer.py','data'],
    excludes = [],
    # We can list binary includes here if our target environment is missing them.
    bin_includes = []
)

executables = [
    Executable(
        'SearchDom.py',
        base = None,
        targetName = 'domain-query.exe',
        #copyDependentFiles = True,
        #compress = True
    )
]

setup(
    name='Domain Search App',
    version = '0.1',
    description = 'Domain Search App',
    options = dict(build_exe = buildOptions),
    executables = executables
)