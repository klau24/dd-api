use DDDB2016Aug;

SHOW TABLES;

-- Public --
select Person.pid, Person.last, Person.first, Person.middle
from Person 
left join Lobbyist ON Person.pid = Lobbyist.pid 
left JOIN servesOn ON Person.pid = servesOn.pid 
where Lobbyist.pid is NULL
and servesOn.pid is NULL;

-- Legislator --
select Person.pid, Person.first, Person.middle, Person.last, Legislator.state, Legislator.twitter_handle, Legislator.capitol_phone, Legislator.room_number 
from Person
inner join Legislator on Person.pid = Legislator.pid;

-- Lobbyist --
SELECT Person.pid, Person.last, Person.first, Lobbyist.state
FROM Person INNER JOIN Lobbyist
ON Person.pid = Lobbyist.pid;

-- Organization --
select Organizations.oid, Organizations.name, Organizations.city, Organizations.stateHeadquartered
from Organizations;

-- Bill --
select Bill.bid, Bill.type, Bill.number, Bill.billState, Bill.status, Bill.house, Bill.state
from Bill;

-- Committee --
select Committee.cid, Committee.house, Committee.name, Committee.type, Committee.state, Committee.short_name, Committee.room, Committee.phone, Committee.fax, Committee.session_year
from Committee;

-- Hearing --
select Hearing.hid, Hearing.date, Hearing.state, Hearing.type, Hearing.session_year
from Hearing;

-- Utterances --
select Utterance.uid, Utterance.text, Utterance.time, Utterance.endTime, Utterance.type, Utterance.alignment, Utterance.state 
from Utterance
where Utterance.current = 1 and Utterance.finalized = 1;

-- Person Spoke Utterance --
select Person.pid, Utterance.uid
from Person
inner join Utterance on Person.pid = Utterance.pid
where Utterance.current = 1 and Utterance.finalized = 1;

-- Lobbyist works_for Organization
select distinct Person.pid, Person.first, Person.last, Person.middle, Organizations.oid, Organizations.name
from Person 
INNER JOIN Lobbyist ON Person.pid = Lobbyist.pid
Inner join LobbyistRepresentation on Person.pid = LobbyistRepresentation.pid
Inner join Organizations on LobbyistRepresentation.oid = Organizations.oid;

-- Organization participates_in Hearing
select LobbyistRepresentation.oid, Organizations.name, Hearing.hid
from LobbyistRepresentation
inner join Organizations on LobbyistRepresentation.oid = Organizations.oid
inner join Hearing on LobbyistRepresentation.hid = Hearing.hid;