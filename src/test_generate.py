import unittest
from generate_page import extract_title
class TestGeneratePage(unittest.TestCase):
    def test_header_extraction(self):
        md = """
This is not a header

- This also isn't

# But this is!
"""
        md2 = """
This is not a header

- This also isn't

#    But this also is!   
"""

        extracted = [extract_title(md), extract_title(md2)]
        correct = ["But this is!", "But this also is!"]
        self.assertListEqual(extracted, correct)
                       

