import collections
import json
import os
import shutil
import subprocess
import unittest
from sys import platform

import approvaltests
import pytest

import collect_library_symbols
from lib_symbols import collect_symbols_and_create_graphs
from relationships import construct_relationships
from collect_library_symbols import get_all_symbols_for_all_dsos

SCRIPT_DIR = os.path.split(__file__)[0]
EXAMPLES_DIR = os.path.join(SCRIPT_DIR, "example_libraries")
EXAMPLES_BUILDDIR = os.path.join(EXAMPLES_DIR, "build")
EXAMPLES_DSOS = os.path.join(EXAMPLES_BUILDDIR, "lib")

GRAPH_OUTPUT_PATH = os.path.join(SCRIPT_DIR, "graphs")


def build_example_dsos():
    if os.path.isdir(EXAMPLES_BUILDDIR):
        shutil.rmtree(EXAMPLES_BUILDDIR)
    os.mkdir(EXAMPLES_BUILDDIR)
    cmake_command = f"cmake {EXAMPLES_DIR}"
    subprocess.run(cmake_command.split(), cwd=EXAMPLES_BUILDDIR)
    subprocess.run("make", cwd=EXAMPLES_BUILDDIR)


@pytest.fixture(autouse=True)
def set_up():
    build_example_dsos()

    if os.path.isdir(GRAPH_OUTPUT_PATH):
        shutil.rmtree(GRAPH_OUTPUT_PATH)

    collect_symbols_and_create_graphs(EXAMPLES_DSOS, GRAPH_OUTPUT_PATH)


def _get_file_path(graph_name):
    file_name = f"dsos.{graph_name}.neato.gv"
    graph_path = os.path.join(GRAPH_OUTPUT_PATH, file_name)
    return graph_path


def test_find_dsos():

    expected = set(['libbaz', 'libfoo', 'libbar'])
    if platform == "darwin":
        expected = [expected + ".dylib" in expected]
    else:
        expected = [expected + ".so" in expected]

    so_files = collect_library_symbols.find_dsos(EXAMPLES_DSOS)

    so_files = [os.path.basename(file) for file in so_files]
    so_files = set(so_files)
    assert expected == so_files


@pytest.mark.parametrize("test_library,defined_symbols",
                         [("libfoo.so", ["foo", "foo2"]),
                          ("libbar.so", ["bar"]),
                          ("libbaz.so", ["baz"])])
def test_get_defined_symbols(test_library, defined_symbols):
    symbol_list = collect_library_symbols.get_defined_symbols(os.path.join(EXAMPLES_DSOS, test_library))

    assert set(symbol_list) == set(defined_symbols)


@pytest.mark.parametrize("test_library,undefined_symbols",
                         [("libfoo.so", ["bar"]),
                          ("libbar.so", ["foo2"]),
                          ("libbaz.so", ["foo2"])])
def test_get_undefined_symbols(test_library, undefined_symbols):
    symbol_list = collect_library_symbols.get_undefined_symbols(os.path.join(EXAMPLES_DSOS, test_library))

    assert set(symbol_list) == set(undefined_symbols)


def test_all():
    approvaltests.verify_file(_get_file_path("all"))


def test_libbar():
    approvaltests.verify_file(_get_file_path("libbar.so"))


def test_libbaz():
    approvaltests.verify_file(_get_file_path("libbaz.so"))


def test_libfoo():
    approvaltests.verify_file(_get_file_path("libfoo.so"))


def test_relationships():
    dsos = get_all_symbols_for_all_dsos(EXAMPLES_DSOS)
    relationships = construct_relationships(dsos)

    all_rels = collections.OrderedDict()
    for rel in relationships.get_all_relations():
        all_rels[f"{rel.from_dso} -> {rel.to_dso}"] = len(rel.symbols)

    approvaltests.verify(json.dumps(all_rels, indent=2))
