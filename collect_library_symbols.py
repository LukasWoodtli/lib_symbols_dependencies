import locale
import os
import subprocess
import pathlib
from sys import platform

import utils
from dso import Dso


@utils.cache_result_to_file("dso_symbols")
def get_all_symbols_for_all_dsos(lib_dir):
    dsos = find_dsos(lib_dir)
    symbols = [get_all_symbols(dso) for dso in dsos]
    return symbols


def get_all_symbols(dso_path):
    print("Processing ", dso_path)
    defined = get_defined_symbols(dso_path)
    undefined = get_undefined_symbols(dso_path)
    return Dso(dso_path, defined, undefined)


FILE_SUFFIX = ".dylib" if platform == "darwin" else ".so"


def find_dsos(path):
    all_dsos = []
    for root, _directories, filenames in os.walk(path):
        for filename in filenames:
            file_path = pathlib.Path(root, filename)
            if file_path.suffix == FILE_SUFFIX:
                all_dsos.append(file_path)
    return set(all_dsos)


def get_undefined_symbols(so_file):
    ret = subprocess.run(["nm",
                          "--undefined-only",
                          "-C",
                          "-f", "posix",
                          so_file],
                         encoding=locale.getdefaultlocale()[1],
                         stdout=subprocess.PIPE,
                         check=True)
    symbols = []
    output = ret.stdout
    output = output.splitlines()
    for line in output:
        print(line)
        fields = line.split()
        assert len(fields) >= 2, fields
        symbol_type = fields[0].strip()
        name = fields[1].strip()
        if symbol_type == "U" and is_useful_symbol(name):
            symbols.append(name)
    return symbols


def get_defined_symbols(so_file):
    ret = subprocess.run(["nm",
                          "--defined-only",
                          "-C",
                          "--extern-only",
                          so_file],
                         encoding=locale.getdefaultlocale()[1],
                         stdout=subprocess.PIPE,
                         check=True)
    symbols = []
    for line in ret.stdout.splitlines():
        fields = line.split()
        assert len(fields) >= 3, fields
        symbol_type = fields[1].strip()
        name = fields[2].strip()
        if symbol_type == "T" and is_useful_symbol(name):
            symbols.append(name)
    return symbols


def is_useful_symbol(sym):
    unused_prefixes = ["_", "std::"]
    for prefix in unused_prefixes:
        if sym.startswith(prefix):
            return False
    charactes_in_unused_symbols = ["@"]
    for char in charactes_in_unused_symbols:
        if char in sym:
            return False
    return True
