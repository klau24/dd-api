import re
import dbConnect
import myCredentials
from flask import Flask, request, jsonify

app = Flask(__name__)

sql_dddb = dbConnect.create_connection(myCredentials.sql_dddb.hostname, myCredentials.sql_dddb.username, myCredentials.sql_dddb.password, myCredentials.sql_dddb.dbname)

@app.route('/')
def test():
    return "Checkout https://github.com/klau24/dd-api for more information"

@app.route('/api/bill/<bid>')
def billSummary(bid):
    # TODO: need video link and time
    # add billPresenter
    res = {"status": 400, 'msg': "", 'data': {} }

    if not bid:
        res['msg'] = "Invalid bid parameter"
        return jsonify(res)

    # General bill information
    query = "select BillVersion.subject, Bill.state, Bill.house, Hearing.date \
            from Bill \
            right join BillVersion on Bill.bid = BillVersion.bid \
            right join BillDiscussion on Bill.bid = BillDiscussion.bid \
            right join Hearing on BillDiscussion.hid = Hearing.hid \
            where Bill.bid = '{bid}' \
            order by Hearing.date desc \
            limit 1;".format(bid=bid)
    cursor = dbConnect.queryDB(sql_dddb, query)
    witnesses = billWitnesses(bid)
    orgAlignment = billOrgAlignment(bid)
    voteSummary = billVoteSummary(bid)
    if cursor and witnesses['status'] == 200 and orgAlignment['status'] == 200 and voteSummary['status'] == 200:
        res['status'] = 200
        for (subject, state, house, date) in cursor:
            res['data']['summary'] = { "subject": subject, "state": state, "house": house, "date": date.strftime('%m/%d/%Y') }
        res['data']['witnesses'] = witnesses['data']['witnesses']
        res['data']['orgAlignment'] = orgAlignment['data']['orgAlignment']
        res['data']['voteSummary'] = {}
        res['data']['voteSummary']['summary'] = voteSummary['data']['summary']
        res['data']['voteSummary']['votes'] = voteSummary['data']['votes']
    return jsonify(res)

def billPresenter(bid):
    pass

def billWitnesses(bid):
    # TODO: need witness position
    res = {"status": 400, 'data': {} }
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

def billOrgAlignment(bid):
    res = {"status": 400, 'data': {} }
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
    res = {"status": 400, 'data': {} }
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
        res['msg'] = 'OK'
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

def getOrg(id):
    pass

def getOrgConcept():
    pass

def getBehest():
    # potential params?: lawmaker, org (payer), org (recipient), chamber, timeLimitation, session, time frame, 
    # Behest: A lawmaker requests a favor from an organization to donate a certain $ to another org
    #   - figure out who gave the money to who
    #   - aggregate by how many request to an org
    pass

@app.route('/api/gift/')
def getGift():
    res = {"status": 400, 'msg': "", 'data': {} }
    first = request.args.get('first')
    last = request.args.get('last')
    source = request.args.get('source')
    op = request.args.get('op')
    value = request.args.get('value')

    if first and not re.match("^[A-Za-z]*$", first):
        res['msg'] = 'Invalid first parameter'
        return jsonify(res)
    if last and not re.match("^[A-Za-z]*$", last):
        res['msg'] = 'Invalid last parameter'
        return jsonify(res)
    if source and not re.match("^[A-Za-z]*$", source):
        res['msg'] = 'Invalid source parameter'
        return jsonify(res)
    if op and not re.match(r'^<|>|=|!=$', op):
        res['msg'] = 'Invalid op parameter'
        return jsonify(res)
    if value and not re.match("^[0-9]+$", value):
        res['msg'] = 'Invalid value parameter'
        return jsonify(res)

    query = "select RecordId, first, last, schedule, sourceName, activity, city, cityState, value, giftDate, description \
            from Gift \
            inner join Person on Person.pid = Gift.pid \
            where "
    conditions = []
    if first:
        conditions.append(f"first='{first.capitalize()}'")
    if last:
        conditions.append(f"last='{last.capitalize()}'")
    if source:
        conditions.append(f"source='{source.title()}'")
    if op and value:
        conditions.append(f"value{op}{value}")
    query += " and ".join(conditions)
    cursor = dbConnect.queryDB(sql_dddb, query)

    if cursor:
        res['status'] = 200
        res['msg'] = 'OK'
        res['data']['gift'] = {}
        count = 0
        for (recordId, first, last, schedule, source, activity, city, state, value, giftDate, description) in cursor:
            res['data']['gift'][count] = {'recordId': recordId, 'first': first, 'last': last, 
                'schedule': schedule, 'source': source, 'activity': activity, 'city': city, 'state': state, 'value': value, 'giftDate': giftDate, 'description': description}
            count += 1
    return jsonify(res)


def is_num(string):
    if string.replace(".", "").isnumeric() or string == "-1":
        return True
    else:
        return False

if __name__ == "__main__":
    app.run(port=8080)
    # res = billSummary("CA_201720180AB569")
    # print(res)
    # res = billWitnesses("TX_20170HB3781")
    # print(res)
    # res = billOrgAlignment("TX_20170HB3781")
    # print(res)
    # res = billVoteSummary("TX_20170HB3781")
    # print(res)
    sql_dddb.close()
