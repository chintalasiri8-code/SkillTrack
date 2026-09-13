"""
Unit tests for Skill Gap Analysis & Priority Engine (backend/analysis.py).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from models import Skill, Project, PlacementFundamental, UserProfile
from analysis import (
    classify_skill,
    calculate_skill_priority,
    generate_skill_recommendation,
    analyze_user_profile
)


class TestAnalysis(unittest.TestCase):
    def test_classify_skill(self):
        self.assertEqual(classify_skill(85), "Strong")
        self.assertEqual(classify_skill(70), "Strong")
        self.assertEqual(classify_skill(69), "Developing")
        self.assertEqual(classify_skill(40), "Developing")
        self.assertEqual(classify_skill(39), "Weak")
        self.assertEqual(classify_skill(0), "Weak")

    def test_priority_logic(self):
        # VERY HIGH: prof < 40, high importance, no project evidence
        p_label, score = calculate_skill_priority(proficiency=25, importance="HIGH", is_demonstrated=False)
        self.assertEqual(p_label, "VERY HIGH")
        self.assertEqual(score, 4)

        # HIGH: prof < 40
        p_label_h, _ = calculate_skill_priority(proficiency=35, importance="MEDIUM", is_demonstrated=True)
        self.assertEqual(p_label_h, "HIGH")

        # LOW: prof >= 70 and demonstrated
        p_label_l, _ = calculate_skill_priority(proficiency=85, importance="HIGH", is_demonstrated=True)
        self.assertEqual(p_label_l, "LOW")

    def test_generate_recommendation(self):
        rec = generate_skill_recommendation("Power BI", 25, "HIGH", False)
        self.assertIn("Improve Power BI", rec)
        self.assertIn("build a project", rec)

    def test_analyze_user_profile(self):
        skills = [
            Skill("Python", 85, "HIGH"),
            Skill("Power BI", 25, "HIGH"),
            Skill("SQL", 55, "MEDIUM")
        ]
        projects = [
            Project("1", "P1", "https://github.com/user/p1", skills_used=["Python"])
        ]
        profile = UserProfile(target_role="Data Analyst", skills=skills, projects=projects)
        analysis = analyze_user_profile(profile)

        self.assertEqual(len(analysis["strong_skills"]), 1)
        self.assertEqual(len(analysis["developing_skills"]), 1)
        self.assertEqual(len(analysis["weak_skills"]), 1)
        self.assertTrue(len(analysis["priority_skills"]) > 0)
        self.assertEqual(analysis["priority_skills"][0]["name"], "Power BI")
        self.assertEqual(analysis["priority_skills"][0]["priority"], "VERY HIGH")


if __name__ == "__main__":
    unittest.main()
