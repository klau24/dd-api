from neo4j import GraphDatabase
import dbConnect
import myCredentials

class Neo4jDDDB:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()

    def addLobbyist(self):
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_Lobbyist)
    
    def addOrganizations(self):
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_Organizations)
    
    def addHearings(self):
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_Hearings)

    @staticmethod
    def _create_and_return_Lobbyist(tx):
        result = tx.run("LOAD CSV WITH HEADERS FROM 'https://github.com/klau24/dd-api/blob/main/data/legislator.csv' AS row "
                        "CREATE (person:Person:Legislator) "
                        "SET person.pid = row.pid"
                        )
        return result
    
    @staticmethod
    def _create_and_return_Organizations(tx):
        result = tx.run("LOAD CSV WITH HEADERS FROM 'https://github.com/klau24/dd-api/blob/main/data/legislator.csv' AS row "
                        "CREATE (person:Person:Legislator) "
                        "SET person.pid = row.pid"
                        )
        return result

    @staticmethod
    def _create_and_return_Hearings(tx):
        result = tx.run("LOAD CSV WITH HEADERS FROM 'https://github.com/klau24/dd-api/blob/main/data/legislator.csv' AS row "
                        "CREATE (person:Person:Legislator) "
                        "SET person.pid = row.pid"
                        )
        return result


if __name__ == "__main__":
    neo4j_dddb = Neo4jDDDB(myCredentials.neo4j_dddb.hostname, myCredentials.neo4j_dddb.username, myCredentials.neo4j_dddb.password)
    neo4j_dddb.addLobbyist()
    neo4j_dddb.addOrganizations()
    neo4j_dddb.addHearings()

    neo4j_dddb.addPersonOrgEdge()
    neo4j_dddb.addOrgHearingEdge()

    neo4j_dddb.close()