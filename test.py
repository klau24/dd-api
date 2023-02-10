from neo4j import GraphDatabase
import dbConnect
import myCredentials

class Neo4jDDDB:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()

    def addLegislators(self):
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_Legislators)

    @staticmethod
    def _create_and_return_Legislators( tx):
        '''
        LOAD CSV WITH HEADERS FROM 'file:///orders.csv' AS row
            MERGE (order:Order {orderID: row.OrderID})
            CREATE SET order.shipName = row.ShipName;
        '''
        result = tx.run("LOAD CSV WITH HEADERS FROM 'file:////Users/Kenny/Desktop/dd-api/data/legislator.csv' AS row "
                        "CREATE (person:Person:Legislator) "
                        "SET person.pid = row.pid"
                        )
        return result


if __name__ == "__main__":
    neo4j_dddb = Neo4jDDDB(myCredentials.neo4j_dddb.hostname, myCredentials.neo4j_dddb.username, myCredentials.neo4j_dddb.password)
    neo4j_dddb.addLegislators()
    neo4j_dddb.close()