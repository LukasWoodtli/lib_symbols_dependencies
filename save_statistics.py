import csv
import os

from relationships import RelationShipStatistic


def save_as_csv(dso_relationships, output_dir):
    relation_stats = dso_relationships.get_relations_stats_for_all_dsos()
    with open(os.path.join(output_dir, "stats.csv"), "w") as csv_file:
        csv_writer = csv.writer(csv_file)

        headers = RelationShipStatistic._fields
        csv_writer.writerow(headers)
        for rel in relation_stats:
            csv_writer.writerow(rel)

