"""
Unit tests for SkillTrack Validation Logic (backend/validation.py).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from models import Skill, Project
from validation import (
    validate_percentage,
    validate_skill,
    validate_github_url,
    validate_project
)


class TestValidation(unittest.TestCase):
    def test_validate_percentage(self):
        valid, msg, val = validate_percentage(75)
        self.assertTrue(valid)
        self.assertEqual(val, 75)

        valid_str, _, val_str = validate_percentage("90")
        self.assertTrue(valid_str)
        self.assertEqual(val_str, 90)

        invalid_out, msg_out, _ = validate_percentage(150)
        self.assertFalse(invalid_out)
        self.assertIn("between 0 and 100", msg_out)

        invalid_type, _, _ = validate_percentage("abc")
        self.assertFalse(invalid_type)

    def test_validate_skill_name_and_duplicate(self):
        existing = [Skill("Python"), Skill("SQL")]
        
        # Empty skill name
        valid, msg = validate_skill("", existing, is_new=True)
        self.assertFalse(valid)

        # Duplicate skill name (case-insensitive)
        valid_dup, msg_dup = validate_skill("python", existing, is_new=True)
        self.assertFalse(valid_dup)
        self.assertIn("already exists", msg_dup)

        # Valid new skill name
        valid_new, _ = validate_skill("Docker", existing, is_new=True)
        self.assertTrue(valid_new)

    def test_validate_github_url(self):
        valid, _ = validate_github_url("https://github.com/example/repo")
        self.assertTrue(valid)

        invalid_empty, msg_e = validate_github_url("")
        self.assertFalse(invalid_empty)

        invalid_link, msg_l = validate_github_url("https://gitlab.com/example/repo")
        self.assertFalse(invalid_link)
        self.assertIn("github.com", msg_l)

    def test_project_limit_enforcement(self):
        # Create 5 existing projects
        projects = [
            Project(str(i), f"P{i}", f"https://github.com/user/p{i}")
            for i in range(1, 6)
        ]

        new_proj_data = {
            "name": "Project 6",
            "github_url": "https://github.com/user/p6"
        }

        # Attempting to add 6th project must fail
        valid, msg = validate_project(new_proj_data, projects, is_update=False)
        self.assertFalse(valid)
        self.assertIn("Maximum limit of 5 projects reached", msg)


if __name__ == "__main__":
    unittest.main()
