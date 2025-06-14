from urllib.request import urlopen
import query_cases
from time import sleep

endpoint = 'http://localhost:8808'


class TestQuery(query_cases.TestCases):

    def probe(self, args, count):
        sleep(2)
        return urlopen(endpoint + args).read(count)
