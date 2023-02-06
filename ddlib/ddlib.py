import dbConnect
import myCredentials
from flask import Flask

app = Flask(__name__)

@app.route('/api/bill/<bid>')
# think about combining billSummary, billPresenter, and billWitnesses into one call
def billSummary(bid):
    # TODO: need video link and time
    res = {"status": 404, 'data': {} }
    query = "select BillVersion.subject, Bill.state, Bill.house, Hearing.date \
            from Bill \
            right join BillVersion on Bill.bid = BillVersion.bid \
            right join BillDiscussion on Bill.bid = BillDiscussion.bid \
            right join Hearing on BillDiscussion.hid = Hearing.hid \
            where Bill.bid = '{bid}' \
            order by Hearing.date desc \
            limit 1;".format(bid=bid)
    cursor = dbConnect.queryDB(sql_dddb, query)
    if cursor:
        res['status'] = 200
        for (subject, state, house, date) in cursor:
            res['data'] = { "subject": subject, "state": state, "house": house, "date": date.strftime('%m/%d/%Y') }
    return res

def billPresenter(bid):
    pass

@app.route('/api/bill/witnesses/<bid>')
def billWitnesses(bid):
    # TODO: need witness position
    res = {"status": 404, 'data': {} }
    query = "select distinct WitnessList.pid, Person.first, Person.last, Organizations.name \
            from WitnessList \
            right join Person on Person.pid = WitnessList.pid \
            right join WitnessListOrganizations on WitnessListOrganizations.wid = WitnessList.wid \
            right join Organizations on Organizations.oid = WitnessListOrganizations.oid \
            where bid = '{bid}';".format(bid=bid)
    cursor = dbConnect.queryDB(sql_dddb, query)
    if cursor:
        res['status'] = 200
        res['data']['witnesses'] = {}
        count = 0
        for (_, first, last, org) in cursor:
            res['data']['witnesses'][count] = {'first': first, 'last': last, 'affiliation': org}
            count += 1
    return res

@app.route('/api/bill/org/alignment/<bid>')
def billOrgAlignment(bid):
    res = {"status": 404, 'data': {} }
    query = "select Organizations.name, WitnessList.position \
            from WitnessList \
            right join Person on Person.pid = WitnessList.pid \
            right join WitnessListOrganizations on WitnessListOrganizations.wid = WitnessList.wid \
            right join Organizations on Organizations.oid = WitnessListOrganizations.oid \
            where bid = '{bid}' \
            group by Organizations.name;".format(bid=bid)
    cursor = dbConnect.queryDB(sql_dddb, query)
    if cursor:
        res['status'] = 200
        res['data']['orgAlignment'] = {}
        count = 0
        for (org, position) in cursor:
            res['data']['orgAlignment'][count] = {'org': org, 'position': position}
            count += 1
    return res

def billVoteSummary(bid):
    res = {"status": 404, 'data': {} }
    query = "select VoteDate, ayes, naes, abstain, result from BillVoteSummary where bid = '{bid}';".format(bid=bid)
    cursor1 = dbConnect.queryDB(sql_dddb, query)
    query = "select Person.first, Person.last, WitnessList.position, Term.party, Term.district, Term.house \
            from WitnessList \
            right join Person on Person.pid = WitnessList.pid \
            right join Legislator on Legislator.pid = WitnessList.pid \
            right join Term on Term.pid = WitnessList.pid \
            where bid = '{bid}';".format(bid=bid)
    cursor2 = dbConnect.queryDB(sql_dddb, query)

    if cursor1 and cursor2:
        res['status'] = 200
        for (date, ayes, naes, abstain, result) in cursor1:
            res['data']['summary'] = {'date': date.strftime('%m/%d/%Y'), 'ayes': ayes, 'naes': naes, 'abstain': abstain, 'result': result}
        res['data']['votes'] = {}
        count = 0
        for (first, last, position, party, district, house) in cursor2:
            res['data']['votes'][count] = {"first": first, "last": last, "position": position, "party": party, "district": district, "house": house}
            count += 1
    return res

def billVideoTranscript(bid):
    # utterance table
    # process to neo4j
    # only grab where current = 1 and finalized = 1

    # given a bill, get all the utterances from the hearing. Utterances should be linked to a person
    pass

def billVideo(bid):
    # Video table
    pass

def billSpeakerParticipation(bid, cutoff):
    # create pie chart data with transcript data
    # participationType: party, personType, etc...
    # experiment with comparing different participationType (use some sort of similarity rating)
    # cutoff is min speaker participation int
    pass

def billRelatedImages(bid):
    pass

def getOrg(id):
    pass

def getOrgConcept():
    pass

def getBehest():
    # params: lawmaker, org (payer), org (recipient), chamber, timeLimitation, session, time frame, 
    # Behest: A lawmaker requests a favor from an organization to donate a certain $ to another org
    #   - figure out who gave the money to who
    #   - aggregate by how many request to an org
    pass

def getGift():
    pass

if __name__ == "__main__":
    sql_dddb = dbConnect.create_connection(myCredentials.sql_dddb.hostname, myCredentials.sql_dddb.username, myCredentials.sql_dddb.password, myCredentials.sql_dddb.dbname)
    app.run(port=5000)
    # res = billSummary("CA_201720180AB569")
    # print(res)
    # res = billWitnesses("TX_20170HB3781")
    # print(res)
    # res = billOrgAlignment("TX_20170HB3781")
    # print(res)
    # res = billVoteSummary("TX_20170HB3781")
    # print(res)
    sql_dddb.close()
