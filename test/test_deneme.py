import unittest
from src.deneme import Deneme

class TestDeneme(unittest.TestCase):
    def test_increment(self):
       deneme = Deneme()
       i = deneme.getI()
       deneme.incr()
       self.assertEqual(i + 1, deneme.getI())

if __name__ == "__main__":
    unittest.main()
