from neo4j.v1 import GraphDatabase, basic_auth, exceptions as neo4jException


class Neo4jDriver:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.driver = None
        self.session = None
        self.result = None

    def connect(self):
        self.driver = GraphDatabase.driver("bolt://" + str(self.host) + ":" + str(self.port),
                                           auth=basic_auth(self.user, self.password))
        self.session = self.driver.session()

    def disconnect(self):
        self.session.close()

    def query(self, query, params=None):
        try:
            if params is not None:
                self.result = self.session.run(query, params)
            else:
                self.result = self.session.run(query)
        except neo4jException:
            raise Neo4jServiceUnavailableError


class Neo4jError(Exception):
    pass


class Neo4jServiceUnavailableError(Exception):
    pass
