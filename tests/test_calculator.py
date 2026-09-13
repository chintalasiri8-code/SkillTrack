"""
Unit tests for SkillTrack Readiness Calculations (backend/calculator.py).
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from models import Skill, Project, PlacementFundamental, UserProfile
from calculator import (
    calculate_skill_readiness,
    calculate_project_coverage,
    calculate_project_readiness,
    calculate_placement_readiness,
    calculate_overall_job_readiness
)


class TestCalculator(unittest.TestCase):
    def test_skill_readiness(self):
        skills = [
            Skill("Python", 80),
            Skill("SQL", 60),
            Skill("Excel", 70)
        ]
        # (80 + 60 + 70) / 3 = 70.0
        self.assertEqual(calculate_skill_readiness(skills), 70.0)

    def test_empty_skill_readiness(self):
        self.assertEqual(calculate_skill_readiness([]), 0.0)

    def test_project_skill_coverage(self):
        required_skills = [
            Skill("Python"), Skill("SQL"), Skill("Excel"),
            Skill("Pandas"), Skill("Power BI"), Skill("Statistics")
        ]
        projects = [
            Project("1", "P1", "https://github.com/user/p1", skills_used=["Python", "SQL"]),
            Project("2", "P2", "https://github.com/user/p2", skills_used=["Excel"]),
            Project("3", "P3", "https://github.com/user/p3", skills_used=["Pandas"]),
            Project("4", "P4", "https://github.com/user/p4", skills_used=["Statistics"]),
        ]
        coverage = calculate_project_coverage(required_skills, projects)
        # 5 demonstrated out of 6 required = (5 / 6) * 100 = 83.33%
        self.assertEqual(coverage["demonstrated_count"], 5)
        self.assertEqual(coverage["total_required"], 6)
        self.assertAlmostEqual(coverage["coverage_percentage"], 83.33, places=1)
        self.assertIn("Power BI", coverage["missing_skills"])

    def test_project_readiness_formula(self):
        required_skills = [Skill("Python"), Skill("SQL")]
        # 5 out of 5 projects with valid GitHub links and 100% skill coverage
        projects = [
            Project(str(i), f"P{i}", "https://github.com/user/repo", skills_used=["Python", "SQL"])
            for i in range(1, 6)
        ]
        readiness_info = calculate_project_readiness(projects, required_skills)
        # Completion: 100 * 0.20 = 20
        # GitHub Evidence: 100 * 0.20 = 20
        # Skill Coverage: 100 * 0.60 = 60
        # Total = 100.0
        self.assertEqual(readiness_info["project_readiness"], 100.0)

    def test_placement_readiness(self):
        fundamentals = [
            PlacementFundamental("DSA", 50),
            PlacementFundamental("OOP", 70)
        ]
        # (50 + 70) / 2 = 60.0
        self.assertEqual(calculate_placement_readiness(fundamentals), 60.0)

    def test_overall_job_readiness(self):
        # Example from requirements section 17:
        # Skill Readiness = 61
        # Project Readiness = 82
        # Placement Readiness = 65
        # Overall = 61 * 0.50 + 82 * 0.30 + 65 * 0.20 = 30.5 + 24.6 + 13 = 68.1 -> rounded = 68
        skills = [Skill("S1", 61)]
        projects = [
            Project("1", "P1", "https://github.com/user/p1", skills_used=["S1"]),
            Project("2", "P2", "https://github.com/user/p2", skills_used=["S1"]),
            Project("3", "P3", "https://github.com/user/p3", skills_used=["S1"]),
            Project("4", "P4", "https://github.com/user/p4", skills_used=["S1"]),
            Project("5", "P5", "https://github.com/user/p5", skills_used=["S1"])
        ]
        fundamentals = [PlacementFundamental("F1", 65)]

        profile = UserProfile(
            target_role="Data Analyst",
            skills=skills,
            projects=projects,
            fundamentals=fundamentals
        )
        res = calculate_overall_job_readiness(profile)
        self.assertEqual(res["skill_readiness"], 61)
        self.assertEqual(res["placement_readiness"], 65)
        self.assertIn("overall_readiness", res)


if __name__ == "__main__":
    unittest.main()
