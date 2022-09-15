#!/usr/bin/env python3
import utils
from collect_library_symbols import get_all_symbols_for_all_dsos
from relationships import construct_relationships
from render_graphs import create_relationship_graphs
from save_statistics import save_as_csv


def collect_symbols_and_create_graphs(lib_dir, output_dir):
    dsos = get_all_symbols_for_all_dsos(lib_dir)
    relationships = construct_relationships(dsos)

    create_relationship_graphs(relationships, output_dir)

    save_as_csv(relationships, ".")


if __name__ == "__main__":
    utils.ENABLE_CACHING = True
    lib_dir = "lib"

    collect_symbols_and_create_graphs(lib_dir, "graphs")
