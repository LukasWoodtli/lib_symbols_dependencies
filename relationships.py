import collections

import utils
from dso import Dso

RelationShip = collections.namedtuple("RelationShip", ["from_dso", "to_dso", "symbols"])
RelationShipStatistic = collections.namedtuple("RelationShipStatistic",
                                               ["dso",
                                                "outgoing_connection",
                                                "incoming_connections"])


class DsoRelationshipMatrix:

    def __init__(self):
        self._all_dsos = []
        self._relationship_data = collections.defaultdict(collections.OrderedDict)

    def add_dso(self, dso: Dso):
        for dso_already_in_data in self._all_dsos:
            self._insert_symbols_for_dsos(dso, dso_already_in_data)
            self._insert_symbols_for_dsos(dso_already_in_data, dso)

        self._relationship_data[dso.get_so_name()][dso.get_so_name()] = {}

        self._all_dsos.append(dso)

    def _insert_symbols_for_dsos(self, from_dso, to_dso):
        from_dso_name = from_dso.get_so_name()
        to_dso_name = to_dso.get_so_name()
        common_symbols = self._get_common_symbols(from_dso, to_dso)

        self._relationship_data[from_dso_name][to_dso_name] = common_symbols

    @staticmethod
    def _get_common_symbols(from_dso, to_dso):
        new_undefined = from_dso.get_undefined_symbols()
        defined = to_dso.get_defined_symbols()
        common_symbols = new_undefined & defined
        return common_symbols

    def get_relations(self, from_, to):
        return self._relationship_data[from_][to]

    def get_all_relations(self):
        rels = []
        for dso_from in self._all_dsos:
            for dso_to in self._all_dsos:
                dso_from_name = dso_from.get_so_name()
                dso_to_name = dso_to.get_so_name()
                if dso_from_name != dso_to_name:
                    symbols = self._relationship_data[dso_from_name][dso_to_name]
                    if len(symbols) > 0:
                        rels.append(RelationShip(dso_from_name,
                                                 dso_to_name,
                                                 symbols))
        return rels

    def get_all_relations_for_dso(self, dso):
        rels = self.get_relations_to_dso(dso)
        rels.extend(self.get_relations_from_dso(dso))

        rels.sort()
        return set(rels)

    def get_relations_from_dso(self, dso):
        rels = []
        for to_dso, symbols in self._relationship_data[dso].items():
            if to_dso != dso:
                if len(symbols) > 0:
                    rels.append(RelationShip(dso,
                                             to_dso,
                                             symbols))
        return rels

    def get_relations_to_dso(self, dso):
        rels = []
        for from_dso, items in self._relationship_data.items():
            if from_dso != dso:
                symbols = items[dso]
                if len(symbols) > 0:
                    rels.append(RelationShip(from_dso,
                                             dso,
                                             symbols))
        return rels

    def get_relations_for_every_single_dso(self):
        rels = collections.OrderedDict()
        for dso in self._all_dsos:
            name = dso.get_so_name()
            rels[name] = self.get_all_relations_for_dso(name)
        return rels

    def get_relations_stats_for_dso(self, dso):
        rels_to_dso = self.get_relations_to_dso(dso)
        num_rels_to_dso = sum([len(rel.symbols) for rel in rels_to_dso])

        rels_from_dso = self.get_relations_from_dso(dso)
        num_rels_from_dso = sum([len(rel.symbols) for rel in rels_from_dso])

        return RelationShipStatistic(dso, num_rels_from_dso, num_rels_to_dso)

    def get_relations_stats_for_all_dsos(self):
        return [self.get_relations_stats_for_dso(dso.get_so_name()) for dso in self._all_dsos]


@utils.cache_result_to_file("dso_relationships")
def construct_relationships(dsos):
    relationships = DsoRelationshipMatrix()
    for dso in dsos:
        relationships.add_dso(dso)
    return relationships
