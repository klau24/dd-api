from neo4j import GraphDatabase
import dbConnect
import myCredentials

class Neo4jDDDB:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        with self.driver.session() as session:
            print("Adding Lobbyist...")
            session.execute_write(self._create_Lobbyist)
            print("Adding Organization...")
            session.execute_write(self._create_Organizations)
            print("Adding Hearing...")
            session.execute_write(self._create_Hearings)
            print("Adding Utterances...")
            session.execute_write(self._create_Utterances)
            print("Adding Person Org Edge...")
            session.execute_write(self._create_LobbyOrgEdge)
            print("Adding Org Hearing Edge...")
            session.execute_write(self._create_OrgHearingEdge)
            print("Adding Person Utterance Edge...")
            session.execute_write(self._create_PersonUtteranceEdge)
        self.driver.close()

    @staticmethod
    def _create_Lobbyist(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/klau24/dd-api/main/data/lobbyist.csv' AS row \
                MERGE (person:Person:Lobbyist {pid: row.pid}) \
                    ON CREATE SET person.first = row.first, person.middle = row.middle, person.last = row.last, person.state = row.state;"
                )
    
    @staticmethod
    def _create_Organizations(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/klau24/dd-api/main/data/organizations.csv' AS row \
                MERGE (org:Organization {oid: row.oid}) \
                    ON CREATE SET org.name = row.name, org.city = row.city;"
                )

    @staticmethod
    def _create_Hearings(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/klau24/dd-api/main/data/hearings.csv' AS row \
                MERGE (hearing:Hearing {hid: row.hid}) \
                    ON CREATE SET hearing.date = row.date, hearing.state = row.state, hearing.type = row.type, hearing.session_year = row.session_year;"
                )

    @staticmethod
    def _create_Utterances(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/klau24/dd-api/main/data/utterances.csv' AS row \
                MERGE (ut:Utterance {uid: row.uid}) \
                    ON CREATE SET ut.text = row.text, ut.time = row.time, ut.endTime = row.endTime, ut.type = row.type, ut.alignment = row.alignment, ut.state = row.state;"
                )

    @staticmethod
    def _create_LobbyOrgEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/klau24/dd-api/main/data/lobbyist_works_for_org.csv' AS row \
                MATCH (person:Person {pid: row.pid}) \
                MATCH (org:Organization {oid: row.oid}) \
                MERGE (person)-[r:WORKS_FOR]->(org);"   
                )

    @staticmethod
    def _create_OrgHearingEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/klau24/dd-api/main/data/organization_participates_in_hearing.csv' AS row \
                MATCH (org:Organization  {oid: row.oid}) \
                MATCH (hearing:Hearing {hid: row.hid}) \
                MERGE (org)-[r:PARTICIPATES_IN]->(hearing);"
                )
    
    @staticmethod
    def _create_PersonUtteranceEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/klau24/dd-api/main/data/person_spoke_utterance.csv' AS row \
                MATCH (person:Person  {pid: row.pid}) \
                MATCH (ut:Utterance {uid: row.uid}) \
                MERGE (person)-[r:SPOKE]->(ut);"
                )

if __name__ == "__main__":
    neo4j_dddb = Neo4jDDDB(myCredentials.neo4j_dddb.hostname, myCredentials.neo4j_dddb.username, myCredentials.neo4j_dddb.password)