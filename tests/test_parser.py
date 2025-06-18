import unittest
from app.parsers.juniper_parser import JuniperParser

class TestJuniperParser(unittest.TestCase):
    def setUp(self):
        self.parser = JuniperParser()

    def test_parse_config(self):
        config = "interfaces { ge-0/0/0 { unit 0 { family inet { address 192.168.1.1/24; } } } }"
        network = self.parser.parse_config(config)
        self.assertIsNotNone(network)

if __name__ == "__main__":
    unittest.main() 