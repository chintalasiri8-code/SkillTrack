"""
Unit tests for SkillTrack Models (backend/models.py).
"""

import unittest
import sys
import os

# Add backend dir to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from models import Skill, Project, PlacementFundamental, JobRole, UserProfile


class TestModels(unittest.TestCase):
    def test_skill_creation_and_dict(self):
        s = Skill(name="Python", proficiency=85, importance="HIGH", is_custom=False)
        self.assertEqual(s.name, "Python")
        self.assertEqual(s.proficiency, 85)
        self.assertEqual(s.importance, "HIGH")
        self.assertFalse(s.is_custom)

        d = s.to_dict()
        s_restored = Skill.from_dict(d)
        self.assertEqual(s_restored.name, "Python")
        self.assertEqual(s_restored.proficiency, 85)

    def test_skill_clamping(self):
        s1 = Skill(name="Overflow", proficiency=150)
        self.assertEqual(s1.proficiency, 100)

        s2 = Skill(name="Underflow", proficiency=-20)
        self.assertEqual(s2.proficiency, 0)

    def test_project_models(self):
        p = Project(
            project_id="1",
            name="Sales Dashboard",
            github_url="https://github.com/user/repo",
            description="Test project",
            skills_used=["Python", "SQL"],
            topics_covered=["Analysis"]
        )
        self.assertEqual(p.name, "Sales Dashboard")
        self.assertEqual(len(p.skills_used), 2)
        
        p_dict = p.to_dict()
        p_restored = Project.from_dict(p_dict)
        self.assertEqual(p_restored.github_url, "https://github.com/user/repo")

    def test_user_profile_serialization(self):
        profile = UserProfile(
            target_role="Data Analyst",
            skills=[Skill("Python", 80)],
            projects=[Project("1", "P1", "https://github.com/user/p1")],
            fundamentals=[PlacementFundamental("DSA", 70)]
        )
        data = profile.to_dict()
        restored = UserProfile.from_dict(data)
        self.assertEqual(restored.target_role, "Data Analyst")
        self.assertEqual(len(restored.skills), 1)
        self.assertEqual(len(restored.projects), 1)
        self.assertEqual(len(restored.fundamentals), 1)


if __name__ == "__main__":
    unittest.main()
