# ddlib Endpoints

## Existing Routes

### Bill

#### `GET /api/bill/bid`

Returns general information about the Bill associated with the `bid`

Example call: `/api/bill/TX_20170HB3781`

```
{
  data: {
    date: "05/19/2017",
    house: "House",
    state: "TX",
    subject: "Relating to the uses of the lifetime license endowment account by the Parks and Wildlife Department.",
    witnesses: {
      "0": {
        "affiliation": "GAME WARDEN PEACE OFFICERS ASSOCIATION",
        "first": "David",
        "last": "Sinclair"
      },
      "1": {
        "affiliation": "Texas Foundation for Conservation and Texas Coalition for Conservation",
        "first": "John",
        "last": "Shepperd"
      },
      ...
    },
    orgAlignment: {
      "0": {
        "org": "Coastal Conservation Association",
        "position": "for"
      },
      "1": {
        "org": "GAME WARDEN PEACE OFFICERS ASSOCIATION",
        "position": "for"
      },
      ...
    },
    voteSummary: {
      "abstain": 2,
      "ayes": 138,
      "date": "05/06/2017",
      "naes": 2,
      "result": "(PASS)",
      votes: {}
    }
  }
  status: 200
}

```
### Video

### Organization

### Gifts & Behest

