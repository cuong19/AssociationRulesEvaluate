from src.common.path import Path
from src.common.yaml import Yaml
from src.common.neo4j_driver import Neo4jDriver, Neo4jServiceUnavailableError


def get_config(path, filename):
    """
    Get the config file
    :param path: usually Path(__file__) to get the path of the current app
    :param filename: name of the config file
    :return: The config variable if succeeded
    """
    try:
        return Yaml(path.get_absolute_path(filename)).content
    except FileNotFoundError:
        return None


def get_transactions_list(config):
    neo4j_driver = Neo4jDriver(host=config['source']['host'], port=config['source']['port'],
                               user=config['source']['user'], password=config['source']['password'])

    print("Connecting to Neo4j database...")
    try:
        neo4j_driver.connect()
        print("OK")
    except ConnectionError:
        print("Failed!")
        return None

    print("Getting data from Neo4j...")
    if neo4j_driver is not None:
        try:
            neo4j_driver.query("MATCH(i:Item)-[:OCCURS_IN]->(t:Transaction) "
                               "RETURN t.uuid, collect(i.name) as item_list")
        except Neo4jServiceUnavailableError:
            print("Failed!")
            return None

        transactions = []
        for record in neo4j_driver.result:
            transaction = []
            for item in record["item_list"]:
                transaction.append(item)
            transactions.append(transaction)
        neo4j_driver.disconnect()
        print("OK")
        return transactions


def rules_evaluate(transactions, config):
    neo4j_driver = Neo4jDriver(host=config['source']['host'], port=config['source']['port'],
                               user=config['source']['user'], password=config['source']['password'])

    print("Connecting to Neo4j database...")
    try:
        neo4j_driver.connect()
        print("OK")
    except ConnectionError:
        print("Failed!")
        return None

    times_rule_found = 0
    times_rules_not_found = 0
    times_rule_applied = 0
    times_rules_not_applied = 0

    it = 0

    if neo4j_driver is not None:
        if transactions is not None:
            for current_transaction in transactions:
                it += 1
                print("Transaction #" + str(it))
                for item in current_transaction:
                    items = [item]

                    neo4j_driver.query("MATCH (ia:Item)-[ra:OCCURS_IN]->(s:ItemSet)-[rc:OCCURS_WITH]->(ic:Item) "
                                       "WHERE ia.name IN {items} "
                                       "AND NOT ic.name IN {items2} "
                                       "WITH s, count(*) as count_ia, "
                                       "rc.lift as lift, rc.support as support, rc.confidence as confidence, "
                                       "ic.name as consequent "
                                       "ORDER BY count_ia DESC, lift DESC, support DESC, confidence DESC "
                                       "RETURN DISTINCT consequent", {"items": items, "items2": items})
                    consequences = []
                    for record in neo4j_driver.result:
                        consequences.append(record["consequent"])

                    if consequences:
                        times_rule_found += 1
                        for consequent in consequences:
                            if consequent in current_transaction:
                                times_rule_applied += 1
                            else:
                                times_rules_not_applied += 1
                    else:
                        times_rules_not_found += 1
                print("Times rule found for an item so far: " + str(times_rule_found))
                print("Times rules not found for an item so far: " + str(times_rules_not_found))
                print("Times rule applied for an item set so far: " + str(times_rule_applied))
                print("Times rule not applied for an item set so far: " + str(times_rules_not_applied))

        neo4j_driver.disconnect()
    return times_rule_found, times_rules_not_found, times_rule_applied, times_rules_not_applied


if __name__ == "__main__":
    # Parse the config file
    conf = get_config(Path(__file__), "config.yml")

    trans = get_transactions_list(conf)

    t_rule_found, t_rules_not_found, t_rule_applied, t_rules_not_applied = rules_evaluate(trans, conf)
    print("Final results:")
    print("Times rule found for an item: " + str(t_rule_found))
    print("Times rules not found for an item: " + str(t_rules_not_found))
    print("Times rule applied for an item set: " + str(t_rule_applied))
    print("Times rule not applied for an item set: " + str(t_rules_not_applied))
