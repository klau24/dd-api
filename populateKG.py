from neo4j import GraphDatabase
import time
import myCredentials

class Neo4jDDDB:

    def __init__(self, uri, user, password):
        start_time = time.time()
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        with self.driver.session() as session:
            # need to clean up csv to have correct quotations
            print("Adding Legislators...")
            session.execute_write(self._create_Legislators)
            print("Adding Lobbyist...")
            session.execute_write(self._create_Lobbyist)
            print("Adding Public...")
            session.execute_write(self._create_Public)
            print("Adding Organization...")
            session.execute_write(self._create_Organizations)
            print("Adding Hearing...")
            session.execute_write(self._create_Hearings)
            print("Adding Utterances...")
            session.execute_write(self._create_Utterances)
            print("Adding Committees...")
            session.execute_write(self._create_Committees)
            print("Adding Bills...")
            session.execute_write(self._create_Bills)
            print("Adding Motion...")
            session.execute_write(self._create_Motion)
            print("Adding BillVersion...")
            # I removed the title, digest, and text from BillVersion. Is it needed?
            session.execute_write(self._create_BillVersion)
            print("Adding Lobbyist Org Edge...")
            session.execute_write(self._create_LobbyOrgEdge)
            print("Adding Org Hearing Edge...")
            session.execute_write(self._create_OrgHearingEdge)
            print("Adding Person Utterance Edge...")
            session.execute_write(self._create_PersonUtteranceEdge)
            print("Adding Legislator Committee Edge...")
            session.execute_write(self._create_LegislatorCommitteeEdge)
            print("Adding Committee Hearing Edge...")
            session.execute_write(self._create_CommitteeHearingEdge)
            print("Adding Bill Hearing Edge...")
            session.execute_write(self._create_BillHearingEdge)
            print("Adding Motion Bill Edge...")
            session.execute_write(self._create_MotionBillEdge)
            print("Adding Bill Version Edge...")
            session.execute_write(self._create_BillHasVersionEdge)
            print("Adding Legislator Motion Edge...")
            session.execute_write(self._create_LegislatorMotionEdge)
            print("Done")
        self.driver.close()
        print("--- %s seconds ---" % (time.time() - start_time))

    @staticmethod
    def _create_Legislators(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/legislator.csv' AS row \
                MERGE (person:Person:Legislator {pid: row.pid}) \
                    ON CREATE SET person.first = row.first, person.middle = row.middle, person.last = row.last, \
                    person.state = row.state, person.twitter_handle = row.twitter_handle, person.capitol_phone = row.capitol_phone, \
                    person.room_number = row.room_number;"
                )
    @staticmethod
    def _create_Lobbyist(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/lobbyist.csv' AS row \
                MERGE (person:Person:Lobbyist {pid: row.pid}) \
                    ON CREATE SET person.first = row.first, person.middle = row.middle, person.last = row.last, person.state = row.state;"
                )

    @staticmethod
    def _create_Public(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/public.csv' AS row \
                MERGE (person:Person:Public {pid: row.pid}) \
                    ON CREATE SET person.first = row.first, person.middle = row.middle, person.last = row.last;"
                )
    
    @staticmethod
    def _create_Organizations(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/organizations.csv' AS row \
                MERGE (org:Organization {oid: row.oid}) \
                    ON CREATE SET org.name = row.name, org.city = row.city;"
                )

    @staticmethod
    def _create_Hearings(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/hearings.csv' AS row \
                MERGE (hearing:Hearing {hid: row.hid}) \
                    ON CREATE SET hearing.date = row.date, hearing.state = row.state, hearing.type = row.type, hearing.session_year = row.session_year;"
                )

    @staticmethod
    def _create_Utterances(tx):
        tx.run("LOAD CSV WITH HEADERS FROM ''https://media.githubusercontent.com/media/klau24/dd-api/main/data/utterances.csv'' AS row \
                MERGE (ut:Utterance {uid: row.uid}) \
                    ON CREATE SET ut.text = row.text, ut.time = row.time, ut.endTime = row.endTime, ut.type = row.type, ut.alignment = row.alignment, ut.state = row.state;"
                )
    
    @staticmethod
    def _create_Committees(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/committee.csv' AS row \
                MERGE (c:Committee {cid: row.cid}) \
                    ON CREATE SET c.name = row.name, c.short_name = row.short_name, c.session_year = row.session_year, c.house = row.house, c.type = row.type, c.state = row.state;"
                )
    
    @staticmethod
    def _create_Bills(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/bill.csv' AS row \
                MERGE (b:Bill {bid: row.bid}) \
                    ON CREATE SET b.type = row.type, b.number = row.number, b.bill_state = row.billState, b.status = row.status, b.house = row.house, b.state = row.state;"
                )

    @staticmethod
    def _create_Motion(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/motion.csv' AS row \
                MERGE (m:Motion {mid: row.mid}) \
                    ON CREATE SET m.text = row.text, m.doPass = row.doPass, m.voteDate = row.VoteDate, m.ayes = row.ayes, m.naes = row.naes, m.abstain = row.abstain, m.result = row.result;"
                )

    @staticmethod
    def _create_BillVersion(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/billVersion.csv' AS row \
                MERGE (bv:BillVersion {vid: row.vid}) \
                    ON CREATE SET bv.bid = row.bid, bv.date = row.date, bv.billState = row.billState, bv.subject = row.subject, bv.state = row.state;"   
                )

    @staticmethod
    def _create_LobbyOrgEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/lobbyist_works_for_org.csv' AS row \
                MATCH (person:Person {pid: row.pid}) \
                MATCH (org:Organization {oid: row.oid}) \
                MERGE (person)-[r:WORKS_FOR]->(org);"   
                )

    @staticmethod
    def _create_OrgHearingEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/organization_participates_in_hearing.csv' AS row \
                MATCH (org:Organization  {oid: row.oid}) \
                MATCH (hearing:Hearing {hid: row.hid}) \
                MERGE (org)-[r:PARTICIPATES_IN]->(hearing);"
                )
    
    @staticmethod
    def _create_PersonUtteranceEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/person_spoke_utterance.csv' AS row \
                MATCH (person:Person  {pid: row.pid}) \
                MATCH (ut:Utterance {uid: row.uid}) \
                MERGE (person)-[r:SPOKE]->(ut);"
                )
    
    @staticmethod
    def _create_LegislatorCommitteeEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/legislator_memberOf_committee.csv' AS row \
                MATCH (person:Person  {pid: row.pid}) \
                MATCH (c:Committee {cid: row.cid, session_year: row.year}) \
                MERGE (person)-[r:IS_MEMBER_OF]->(c);"
                )
    
    @staticmethod
    def _create_CommitteeHearingEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/committee_presentAt_hearing.csv' AS row \
                MATCH (c:Committee  {cid: row.cid}) \
                MATCH (h:Hearing {hid: row.hid}) \
                MERGE (c)-[r:PRESENT_AT]->(h);"
                )

    @staticmethod
    def _create_BillHearingEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/bill_isDiscussedIn_hearing.csv' AS row \
                MATCH (b:Bill  {bid: row.bid}) \
                MATCH (h:Hearing {hid: row.hid}) \
                MERGE (b)-[r:IS_DISCUSSED_IN]->(h);"
                )

    @staticmethod
    def _create_MotionBillEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/motion.csv' AS row \
                MATCH (m:Motion {mid: row.mid}) \
                MATCH (b:Bill {bid: row.bid}) \
                MERGE (m)-[r:RELATES_TO]->(b);"
                )
    
    @staticmethod
    def _create_BillHasVersionEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/billVersion.csv' AS row \
                MATCH (b:Bill {bid: row.bid}) \
                MATCH (bv:BillVersion {vid: row.vid}) \
                MERGE (b)-[r:HAS]->(bv);"
                )
    
    @staticmethod
    def _create_LegislatorMotionEdge(tx):
        tx.run("LOAD CSV WITH HEADERS FROM 'https://media.githubusercontent.com/media/klau24/dd-api/main/data/legislator_votes_motion.csv' AS row \
                MATCH (p:Person {pid: row.pid}) \
                MATCH (m:Motion {mid: row.mid}) \
                MERGE (p)-[r:VOTES]->(m);"
                )

if __name__ == "__main__":
    neo4j_dddb = Neo4jDDDB(myCredentials.neo4j_dddb.hostname, myCredentials.neo4j_dddb.username, myCredentials.neo4j_dddb.password)