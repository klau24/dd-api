from neo4j import GraphDatabase
import dbConnect
import myCredentials

class Neo4jDDDB:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()

    def addLobbyist(self):
        print("Adding Lobbyist...")
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_Lobbyist)
    
    def addOrganizations(self):
        print("Adding Organization...")
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_Organizations)
    
    def addHearings(self):
        print("Adding Hearing...")
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_Hearings)
    
    def addPersonOrgEdge(self):
        print("Adding Person Org Edge...")
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_PersonOrgEdge)
    
    def addOrgHearingEdge(self):
        print("Adding Org Hearing Edge...")
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_OrgHearingEdge)

    @staticmethod
    def _create_and_return_Lobbyist(tx):
        tx.run("LOAD CSV FROM 'https://github.com/klau24/dd-api/blob/main/data/test.csv' AS row \
                MERGE (person:Person:Lobbyist {pid: row[0]}) \
                ON CREATE SET person.first = row[2], person.last = row[1], person.state = row[3]"
                )
    
    @staticmethod
    def _create_and_return_Organizations(tx):
        result = tx.run("LOAD CSV WITH HEADERS FROM 'https://github.com/klau24/dd-api/blob/main/data/organizations.csv' AS row "
                        "CREATE (org:Organization) "
                        "SET org.oid = row.oid "
                        "SET org.city = row.city"
                        )
        return result

    @staticmethod
    def _create_and_return_Hearings(tx):
        result = tx.run("LOAD CSV WITH HEADERS FROM 'https://github.com/klau24/dd-api/blob/main/data/hearings.csv' AS row "
                        "CREATE (hearing:Hearing) "
                        "SET hearing.hid = row.hid "
                        "SET hearing.date = row.date "
                        "SET hearing.state = row.state "
                        "SET hearing.type = row.type "
                        "SET hearing.session_year = row.session_year"
                        )
        return result

    @staticmethod
    def _create_and_return_PersonOrgEdge(tx):
        result = tx.run("LOAD CSV WITH HEADERS FROM 'https://github.com/klau24/dd-api/blob/main/data/lobbyist_works_for_org.csv' AS row "
                        "MATCH (person:Person), (org:Organization) "
                        "WHERE person.pid = row.pid AND org.oid = row.oid "
                        "CREATE (person)-[r:WORKS_FOR]->(org)"
                        )
        return result

    @staticmethod
    def _create_and_return_OrgHearingEdge(tx):
        result = tx.run("LOAD CSV WITH HEADERS FROM 'https://github.com/klau24/dd-api/blob/main/data/organization_participates_in_hearing.csv' AS row "
                        "MATCH (org:Organization), (hearing:Hearing) "
                        "WHERE org.oid = row.oid AND hearing.hid = row.hid "
                        "CREATE (org)-[r:PARTICIPATES_IN]->(hearing)"
                        )
        return result


if __name__ == "__main__":
    neo4j_dddb = Neo4jDDDB(myCredentials.neo4j_dddb.hostname, myCredentials.neo4j_dddb.username, myCredentials.neo4j_dddb.password)
    neo4j_dddb.addLobbyist()
    #neo4j_dddb.addOrganizations()
    #neo4j_dddb.addHearings()

    #neo4j_dddb.addPersonOrgEdge()
    #neo4j_dddb.addOrgHearingEdge()

    neo4j_dddb.close()