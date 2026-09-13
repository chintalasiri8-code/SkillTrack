"""
Unit tests for SkillTrack Storage Layer (backend/storage.py).
"""

import unittest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from models import UserProfile, Skill
from storage import load_roles, load_user_data, save_user_data


class TestStorage(unittest.TestCase):
    def test_load_roles(self):
        roles = load_roles()
        self.assertTrue(len(roles) >= 2)
        role_names = [r.role_name for r in roles]
        self.assertIn("Data Analyst", role_names)
        self.assertIn("Web Developer", role_names)

    def test_load_and_save_user_data(self):
        profile = load_user_data()
        self.assertIsNotNone(profile)
        self.assertTrue(hasattr(profile, "target_role"))

        # Modify and save
        original_role = profile.target_role
        profile.target_role = original_role
        saved = save_user_data(profile)
        self.assertTrue(saved)

        reloaded = load_user_data()
        self.assertEqual(reloaded.target_role, original_role)


if __name__ == "__main__":
    unittest.main()
