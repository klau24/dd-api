# dd-api

An API to access the Digital Democracy database and knowledge graph. Work in progress...

# TODO

- [ ] Create separate flask modules 
- [ ] Setup prettier
- [ ] add a TOC to this md file

# Existing Routes

### Bill

#### `GET /api/bill/<bid>`

Returns general, organization alignment, voteing, and witness information about the Bill associated with the `<bid>`

Example call: `/api/bill/TX_20170HB3781`

```
{
  data: {
    orgAlignment: {
      0: {
        org	"Coastal Conservation Association"
        position	"for"
      },
      1: {
        org	"GAME WARDEN PEACE OFFICERS ASSOCIATION"
        position	"for"
      },
      ...
    },
    summary: {
      date: "05/19/2017"
      house: "House"
      state: "TX"
      subject: "Relating to the uses of the lifetime license endowment account by the Parks and Wildlife Department."
    },
    voteSummary: {
      summary: {
        abstain: 2
        ayes: 138
        date: "05/06/2017"
        naes: 2
        result: "(PASS)"
      },
      votes: {}
    },
    witnesses: {
      0: {
        affiliation: "GAME WARDEN PEACE OFFICERS ASSOCIATION"
        first: "David"
        last: "Sinclair"
      },
      1: {
        affiliation: "Texas Foundation for Conservation and Texas Coalition for Conservation"
        first: "John"
        last: "Shepperd"
      }
    }
  },
  msg: "OK",
  status: 200
}

```

### Gifts

#### `GET /api/gift/`

Returns gift information

**Parameters**

`first`: First name of gift recipient

`last`: Last name of gift recipient

`source`: The source organization that provided the gift

`op`: Operator in `[< > = !=]`

`value`: Monetary value of gift

Example call: `/api/gift/?first=luis&op=>&value=100`

```
{
  data: {
    gift: {
      0: {
        activity: "Tribal"
        city: "Sacramento"
        description: "Dinner/Hotel\n"
        first: "Luis"
        giftDate: "Wed, 31 Jul 2013 00:00:00 GMT"
        last: "Alejo"
        recordId: 2
        schedule: "E"
        source: "California Tribal Alliance"
        state: "CA"
        value: 252.6999969482422
      },
      1: {
        activity: "Tribal"
        city: "Sacramento"
        description: "Dinner/Hotel\n"
        first: "Luis"
        giftDate: "Wed, 04 Sep 2013 00:00:00 GMT"
        last: "Alejo"
        recordId: 3
        schedule: "E"
        source: "California Tribal Alliance"
        state: "CA"
        value: 147.14999389648438
      },
      ...
    }
  }
  msg: "OK",
  status: 200
}
```
