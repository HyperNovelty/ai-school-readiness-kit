import unittest

from scripts.render_readiness_card_html import render_card_html
from tests.test_validate_readiness_card import valid_card


class RenderReadinessCardHtmlTest(unittest.TestCase):
    def test_render_escapes_html(self):
        card = valid_card()
        card["title"] = "<Synthetic & Card>"
        card["equity_access_notes"] = ["Avoid <script>alert(1)</script> content."]
        rendered = render_card_html(card)
        self.assertIn("&lt;Synthetic &amp; Card&gt;", rendered)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", rendered)
        self.assertNotIn("<script>alert(1)</script>", rendered)

    def test_render_includes_core_sections(self):
        rendered = render_card_html(valid_card())
        self.assertIn("Summary", rendered)
        self.assertIn("Equity and Access Notes", rendered)
        self.assertIn("Human Review Steps", rendered)
        self.assertIn("Not For", rendered)


if __name__ == "__main__":
    unittest.main()

