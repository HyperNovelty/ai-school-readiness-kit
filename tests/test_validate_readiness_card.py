import unittest

from scripts.validate_readiness_card import validate_card


def valid_card():
    return {
        "card_id": "synthetic-001",
        "title": "Synthetic Card",
        "school_context": "Synthetic classroom context",
        "audience": "Teacher and family reviewer",
        "ai_use_case": "AI drafts practice feedback for human review.",
        "student_data_involved": False,
        "assessment_impact": "No assessment impact.",
        "equity_access_notes": ["Non-AI path is available."],
        "human_review_steps": [],
        "family_communication_needed": False,
        "not_for": ["Not for grading."],
        "review_status": "draft",
    }


class ValidateReadinessCardTest(unittest.TestCase):
    def test_valid_card(self):
        self.assertEqual(validate_card(valid_card()), [])

    def test_student_data_requires_review_steps_and_family_communication(self):
        card = valid_card()
        card["student_data_involved"] = True
        errors = validate_card(card)
        self.assertIn(
            "student_data_involved requires at least one human_review_steps item",
            errors,
        )
        self.assertIn(
            "student_data_involved requires family_communication_needed to be true",
            errors,
        )

    def test_allowed_review_status(self):
        card = valid_card()
        card["review_status"] = "approved"
        errors = validate_card(card)
        self.assertTrue(any("review_status must be one of" in error for error in errors))

    def test_array_items_must_be_strings(self):
        card = valid_card()
        card["not_for"] = ["Not for grading.", 42]
        self.assertIn("not_for[1] must be str", validate_card(card))


if __name__ == "__main__":
    unittest.main()

