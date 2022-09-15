import collections

import pytest

from dso import Dso
from relationships import RelationShip, RelationShipStatistic, DsoRelationshipMatrix


@pytest.fixture
def relationship_matrix():
    first_dso = Dso("test1",
                    defined_symbols=["symbol_1", "symbol_2"],
                    undefined_symbols=["symbol_a", "symbol_b", "symbol_c"])
    second_dso = Dso("test2",
                     defined_symbols=["symbol_a", "symbol_c"],
                     undefined_symbols=["symbol_1"])
    third_dso = Dso("test3",
                    defined_symbols=["symbol_x", "symbol_b"],
                    undefined_symbols=["symbol_c"])

    matrix = DsoRelationshipMatrix()
    matrix.add_dso(first_dso)
    matrix.add_dso(second_dso)
    matrix.add_dso(third_dso)
    return matrix


def test_relationship_fom_1_to_2(relationship_matrix):
    rel = relationship_matrix.get_relations(from_="test1", to="test2")
    assert rel == {"symbol_a", "symbol_c"}


def test_relationship_fom_2_to_1(relationship_matrix):
    rel = relationship_matrix.get_relations(from_="test2", to="test1")
    assert rel == {"symbol_1"}


def test_relationship_fom_1_to_1(relationship_matrix):
    rel = relationship_matrix.get_relations(from_="test1", to="test1")
    assert rel == {}


def test_relationship_fom_2_to_2(relationship_matrix):
    rel = relationship_matrix.get_relations(from_="test2", to="test2")
    assert rel == {}


def test_get_all_relations(relationship_matrix):
    rels = relationship_matrix.get_all_relations()
    expected_rels = [RelationShip("test1", "test2", {"symbol_a", "symbol_c"}),
                     RelationShip("test1", "test3", {"symbol_b"}),
                     RelationShip("test2", "test1", {"symbol_1"}),
                     RelationShip("test3", "test2", {"symbol_c"})]

    assert rels == expected_rels


def test_get_relations_for_dso_1(relationship_matrix):
    rels = relationship_matrix.get_all_relations_for_dso("test1")
    expected_rels = {RelationShip("test1", "test2", frozenset({"symbol_a", "symbol_c"})),
                     RelationShip("test1", "test3", frozenset({"symbol_b"})),
                     RelationShip("test2", "test1", frozenset({"symbol_1"}))}

    assert rels == expected_rels


def test_get_relations_for_every_single_dso(relationship_matrix):
    rels = collections.OrderedDict(relationship_matrix.get_relations_for_every_single_dso())
    expected_rels = collections.OrderedDict(
        {"test1": {RelationShip("test1", "test2", frozenset({"symbol_a", "symbol_c"})),
                   RelationShip("test1", "test3", frozenset({"symbol_b"})),
                   RelationShip("test2", "test1", frozenset({"symbol_1"}))},
         "test2": {RelationShip("test1", "test2", frozenset({"symbol_a", "symbol_c"})),
                   RelationShip("test2", "test1", frozenset({"symbol_1"})),
                   RelationShip("test3", "test2", frozenset({"symbol_c"}))},
         "test3": {RelationShip("test1", "test3", frozenset({"symbol_b"})),
                   RelationShip("test3", "test2", frozenset({"symbol_c"}))}
         })

    assert rels == expected_rels


def test_get_relations_to_dso(relationship_matrix):
    rel = relationship_matrix.get_relations_to_dso("test1")

    expected = [RelationShip("test2", "test1", frozenset({"symbol_1"}))]

    assert rel == expected


def test_get_relations_from_dso(relationship_matrix):
    rel = relationship_matrix.get_relations_from_dso("test1")

    expected = [RelationShip("test1", "test2", frozenset({"symbol_a", "symbol_c"})),
                RelationShip("test1", "test3", frozenset({"symbol_b"}))]

    assert rel == expected


def test_get_relations_stats_for_dso(relationship_matrix):
    stat = relationship_matrix.get_relations_stats_for_dso("test1")

    expected = RelationShipStatistic("test1", 3, 1)

    assert stat == expected


def test_get_relations_stats_for_all_dsos(relationship_matrix):
    stat = relationship_matrix.get_relations_stats_for_all_dsos()

    expected = [RelationShipStatistic("test1", 3, 1),
                RelationShipStatistic("test2", 1, 3),
                RelationShipStatistic("test3", 1, 1)]

    assert stat == expected
