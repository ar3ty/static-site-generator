import unittest

from fillespages import extract_title

class TestTitleExtraction(unittest.TestCase):
    def test_simple(self):
        md = """
# This is heading
"""
        self.assertEqual(extract_title(md), "This is heading")

    def test_error(self):
        md = """
## This is not valid heading
"""
        self.assertRaises(Exception, lambda: extract_title(md))

if __name__ == "__main__":
    unittest.main()