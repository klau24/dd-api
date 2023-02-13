from neo4j import GraphDatabase
import dbConnect
import myCredentials

class Neo4jDDDB:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def addLobbyists(self, pid, last, first, middle, filer_id, state):
        with self.driver.session() as session:
            lobbyist = session.execute_write(self._create_and_return_Lobbyists, pid, last, first, middle, filer_id, state)
            print(lobbyist)


    def addLegislators(self, pid, last, first, middle, year, house, cid, state, position):
        with self.driver.session() as session:
            legislator = session.execute_write(self._create_and_return_Legislators, pid, last, first, middle, year, house, cid, state, position)
            print(legislator)
    
    def addPublic(self, pid, last, first, middle):
        with self.driver.session() as session:
            public = session.execute_write(self._create_and_return_Public, pid, last, first, middle)
            print(public)
    
    def addCommittee(self, cid, house, name, type, state, short_name, room, phone, fax, session_year):
        with self.driver.session() as session:
            committee = session.execute_write(self._create_and_return_Committee, cid, house, name, type, state, short_name, room, phone, fax, session_year)
            print(committee)
    
    def addCommitteeHearing(self, dr_id, cid, hid):
        with self.driver.session() as session:
            hearing = session.execute_write(self._create_and_return_CommitteeHearing, dr_id, cid, hid)
            print(hearing)
    
    def addHearing(self, hid, date, state, type, session_year):
        with self.driver.session() as session:
            hearing = session.execute_write(self._create_and_return_Hearing, hid, date, state, type, session_year)
            print(hearing)
    
    def addOrganization(self, oid, name, city, stateHeadquartered):
        with self.driver.session() as session:
            org = session.execute_write(self._create_and_return_Org, oid, name, city, stateHeadquartered)
            print(org)
    
    def addBill(self, bid, type, number, billState, status, house, state):
        with self.driver.session() as session:
            bill = session.execute_write(self._create_and_return_Bill, bid, type, number, billState, status, house, state)
            print(bill)

    @staticmethod
    def _create_and_return_Lobbyists(tx, pid, last, first, middle, filer_id, state):
        result = tx.run("CREATE (a:Person:Lobbyist) "
                        "SET a.pid = $pid "
                        "SET a.first = $first "
                        "SET a.last = $last "
                        "SET a.middle = $middle "
                        "SET a.filer_id = $filer_id "
                        "SET a.state = $state "
                        "RETURN a.first + a.last + ', from node ' + id(a)", pid=pid, first=first, last=last, middle=middle, filer_id=filer_id, state=state)
        return result.single()[0]
    
    @staticmethod
    def _create_and_return_Legislators(tx, pid, last, first, middle, year, house, cid, state, position):
        result = tx.run("CREATE (a:Person:Legislator) "
                        "SET a.pid = $pid "
                        "SET a.first = $first "
                        "SET a.last = $last "
                        "SET a.middle = $middle "
                        "SET a.year = $year "
                        "SET a.house = $house "
                        "SET a.cid = $cid "
                        "SET a.state = $state "
                        "SET a.position = $position "
                        "RETURN a.first + a.last + ', from node ' + id(a)", pid=pid, first=first, last=last, middle=middle, year=year, house=house, cid=cid, state=state, position=position)
        return result.single()[0]
    
    @staticmethod
    def _create_and_return_Public(tx, pid, last, first, middle):
        result = tx.run("CREATE (a:Person:Public) "
                        "SET a.pid = $pid "
                        "SET a.first = $first "
                        "SET a.last = $last "
                        "SET a.middle = $middle "
                        "RETURN a.first + a.last + ', from node ' + id(a)", pid=pid, first=first, last=last, middle=middle)
        return result.single()[0]
    
    @staticmethod
    def _create_and_return_Committee(tx, cid, house, name, type, state, short_name, room, phone, fax, session_year):
        result = tx.run("CREATE (a:Committee) "
                        "SET a.cid = $cid "
                        "SET a.house = $house "
                        "SET a.name = $name "
                        "SET a.type = $type "
                        "SET a.state = $state "
                        "SET a.short_name = $short_name "
                        "SET a.room = $room "
                        "SET a.phone = $phone "
                        "SET a.fax = $fax "
                        "SET a.session_year = $session_year "
                        "RETURN a.house + a.name + ', from node ' + id(a)", cid=cid, house=house, name=name, type=type, state=state, short_name=short_name, room=room, phone=phone, fax=fax, session_year=session_year)
        return result.single()[0]

    @staticmethod
    def _create_and_return_CommitteeHearing(tx, dr_id, cid, hid):
        result = tx.run("CREATE (a:CommitteeHearing) "
                        "SET a.dr_id = $dr_id "
                        "SET a.cid = $cid "
                        "SET a.hid = $hid "
                        "RETURN a.dr_id + a.cid + ', from node ' + id(a)", dr_id=dr_id, cid=cid, hid=hid)
        return result.single()[0]
    
    @staticmethod
    def _create_and_return_Hearing(tx, hid, date, state, type, session_year):
        result = tx.run("CREATE (a:CommitteeHearing) "
                        "SET a.hid = $hid "
                        "SET a.date = $date "
                        "SET a.state = $state "
                        "SET a.type = $type "
                        "SET a.session_year = $session_year "
                        "RETURN a.hid + a.date + a.state + a.type + a.session_year', from node ' + id(a)", hid=hid, date=date, state=state, type=type, session_year=session_year)
        return result.single()[0]
    
    @staticmethod
    def _create_and_return_Org(tx, oid, name, city, stateHeadquartered):
        result = tx.run("CREATE (a:Organization) "
                        "SET a.oid = $oid "
                        "SET a.name = $name "
                        "SET a.city = $city "
                        "SET a.stateHeadquartered = $stateHeadquartered "
                        "RETURN a.name + a.city + ', from node ' + id(a)", oid=oid, name=name, city=city, stateHeadquartered=stateHeadquartered)
        return result.single()[0]

    @staticmethod
    def _create_and_return_Bill(tx, bid, type, number, billState, status, house, state):
        result = tx.run("CREATE (a:Bill) "
                        "SET a.bid = $bid "
                        "SET a.type = $type "
                        "SET a.number = $number "
                        "SET a.billState = $billState "
                        "SET a.status = $status "
                        "SET a.house = $house "
                        "SET a.state = $state "
                        "RETURN a.bid + a.type + a.number + a.billState + a.status + a.house + a.state', from node ' + id(a)", bid=bid, type=type, number=number, billState=billState, status=status, house=house, state=state)
        return result.single()[0]

if __name__ == "__main__":
    neo4j_dddb = Neo4jDDDB(myCredentials.neo4j_dddb.hostname, myCredentials.neo4j_dddb.username, myCredentials.neo4j_dddb.password)
    sql_dddb = dbConnect.create_connection(myCredentials.sql_dddb.hostname, myCredentials.sql_dddb.username, myCredentials.sql_dddb.password, myCredentials.sql_dddb.dbname)

    # Add Lobbyists
    cursor = dbConnect.queryDB(sql_dddb, "SELECT Person.pid, Person.last, Person.first, Person.middle, Lobbyist.filer_id, Lobbyist.state \
        FROM Person INNER JOIN Lobbyist \
        ON Person.pid = Lobbyist.pid;")
    for (pid, last, first, middle, filer_id, state) in cursor:
        neo4j_dddb.addLobbyists(pid, last, first, middle, filer_id, state)
    
    # Add Legislators
    cursor = dbConnect.queryDB(sql_dddb, "SELECT Person.pid, Person.last, Person.first, Person.middle, servesOn.year, servesOn.house, servesOn.cid, servesOn.state, servesOn.position \
        FROM Person \
        INNER JOIN servesOn ON Person.pid = servesOn.pid;")
    for (pid, last, first, middle, year, house, cid, state, position) in cursor:
        neo4j_dddb.addLegislators(pid, last, first, middle, year, house, cid, state, position)

    # Add Public
    cursor = dbConnect.queryDB(sql_dddb, "select Person.pid, Person.last, Person.first, Person.middle \
        from Person \
        left join Lobbyist ON Person.pid = Lobbyist.pid \
        left JOIN servesOn ON Person.pid = servesOn.pid \
        where Lobbyist.pid is NULL \
        and servesOn.pid is NULL;")
    for (pid, last, first, middle) in cursor:
        neo4j_dddb.addPublic(pid, last, first, middle)

    # Add Committee
    cursor = dbConnect.queryDB(sql_dddb, "select Committee.cid, Committee.house, Committee.name, Committee.type, Committee.state, Committee.short_name, Committee.room, Committee.phone, Committee.fax, Committee.session_year \
        from Committee;")
    for (cid, house, name, type, state, short_name, room, phone, fax, session_year) in cursor:
        neo4j_dddb.addCommittee(cid, house, name, type, state, short_name, room, phone, fax, session_year)

    # Add Committee Hearing
    cursor = dbConnect.queryDB(sql_dddb, "select CommitteeHearings.dr_id, CommitteeHearings.cid, CommitteeHearings.hid \
        from CommitteeHearings;")
    for (dr_id, cid, hid) in cursor:
        neo4j_dddb.addCommitteeHearing(dr_id, cid, hid)

    # Add Hearing
    cursor = dbConnect.queryDB(sql_dddb, "select Hearing.hid, Hearing.date, Hearing.state, Hearing.type, Hearing.session_year \
        from Hearing;")
    for (hid, date, state, type, session_year) in cursor:
        neo4j_dddb.addHearing(hid, date, state, type, session_year)

    # Add Bill
    cursor = dbConnect.queryDB(sql_dddb, "select Bill.bid, Bill.type, Bill.number, Bill.billState, Bill.status, Bill.house, Bill.state \
        from Bill;")
    for (bid, type, number, billState, status, house, state) in cursor:
        neo4j_dddb.addBill(bid, type, number, billState, status, house, state)

    # Add Organization
    cursor = dbConnect.queryDB(sql_dddb, "select Organizations.oid, Organizations.name, Organizations.city, Organizations.stateHeadquartered \
        from Organizations;")
    for (oid, name, city, stateHeadquartered) in cursor:
        neo4j_dddb.addOrganization(oid, name, city, stateHeadquartered)

    sql_dddb.close()
    neo4j_dddb.close()