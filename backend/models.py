"""
SkillTrack Data Models
Core Python OOP classes for representing skills, projects, placement fundamentals, roles, and user profiles.
"""


class Skill:
    def __init__(self, name, proficiency=0, importance="MEDIUM", is_custom=False):
        self.name = name
        self.proficiency = max(0, min(100, int(proficiency)))
        self.importance = importance if importance in ["HIGH", "MEDIUM", "LOW"] else "MEDIUM"
        self.is_custom = is_custom

    def to_dict(self):
        return {
            "name": self.name,
            "proficiency": self.proficiency,
            "importance": self.importance,
            "is_custom": self.is_custom
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            proficiency=data.get("proficiency", 0),
            importance=data.get("importance", "MEDIUM"),
            is_custom=data.get("is_custom", False)
        )


class Project:
    def __init__(self, project_id, name, github_url, description="", skills_used=None, topics_covered=None):
        self.project_id = str(project_id)
        self.name = name
        self.github_url = github_url
        self.description = description
        self.skills_used = skills_used if skills_used is not None else []
        self.topics_covered = topics_covered if topics_covered is not None else []

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "name": self.name,
            "github_url": self.github_url,
            "description": self.description,
            "skills_used": self.skills_used,
            "topics_covered": self.topics_covered
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            project_id=data.get("project_id", ""),
            name=data.get("name", ""),
            github_url=data.get("github_url", ""),
            description=data.get("description", ""),
            skills_used=data.get("skills_used", []),
            topics_covered=data.get("topics_covered", [])
        )


class PlacementFundamental:
    def __init__(self, name, proficiency=0):
        self.name = name
        self.proficiency = max(0, min(100, int(proficiency)))

    def to_dict(self):
        return {
            "name": self.name,
            "proficiency": self.proficiency
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            proficiency=data.get("proficiency", 0)
        )


class JobRole:
    def __init__(self, role_id, role_name, default_skills=None):
        self.role_id = role_id
        self.role_name = role_name
        self.default_skills = default_skills if default_skills is not None else []

    def to_dict(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name,
            "default_skills": [skill.to_dict() for skill in self.default_skills]
        }

    @classmethod
    def from_dict(cls, data):
        skills = [Skill.from_dict(s) for s in data.get("default_skills", [])]
        return cls(
            role_id=data.get("role_id", ""),
            role_name=data.get("role_name", ""),
            default_skills=skills
        )


class UserProfile:
    def __init__(self, target_role="Data Analyst", skills=None, projects=None, fundamentals=None):
        self.target_role = target_role
        self.skills = skills if skills is not None else []
        self.projects = projects if projects is not None else []
        self.fundamentals = fundamentals if fundamentals is not None else []

    def to_dict(self):
        return {
            "target_role": self.target_role,
            "skills": [s.to_dict() for s in self.skills],
            "projects": [p.to_dict() for p in self.projects],
            "fundamentals": [f.to_dict() for f in self.fundamentals]
        }

    @classmethod
    def from_dict(cls, data):
        skills = [Skill.from_dict(s) for s in data.get("skills", [])]
        projects = [Project.from_dict(p) for p in data.get("projects", [])]
        fundamentals = [PlacementFundamental.from_dict(f) for f in data.get("fundamentals", [])]
        return cls(
            target_role=data.get("target_role", "Data Analyst"),
            skills=skills,
            projects=projects,
            fundamentals=fundamentals
        )
