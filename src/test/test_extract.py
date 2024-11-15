from unittest import TestCase, main
from lib.extract_markdown import extract_title

class TestExtractTitle(TestCase):
    def test_case(self):
        text = "# Heading \n### Heading 3"
        self.assertEqual( extract_title(text), "Heading" )


if __name__ == "__main__":
    main()
