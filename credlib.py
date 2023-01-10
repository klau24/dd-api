class Credential:
    def __init__(self, hostname, username, password, dbname=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.dbname = dbname