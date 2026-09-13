"""
SkillTrack JSON Storage Layer
Handles reading/writing roles and user data with exception handling.
"""

import json
import os
from models import UserProfile, JobRole, Skill, PlacementFundamental

# Base directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ROLES_FILE = os.path.join(DATA_DIR, "roles.json")
USER_DATA_FILE = os.path.join(DATA_DIR, "user_data.json")


def ensure_data_directory():
    """Ensure data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def load_roles():
    """
    Load job roles template from roles.json.
    Returns list of JobRole objects.
    """
    ensure_data_directory()
    if not os.path.exists(ROLES_FILE):
        return []
    
    try:
        with open(ROLES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            roles_list = data.get("roles", [])
            return [JobRole.from_dict(r) for r in roles_list]
    except Exception as e:
        print(f"[Storage Error] Failed to load roles: {e}")
        return []


def get_default_fundamentals():
    """Default placement fundamentals list."""
    default_names = [
        "Aptitude", "Communication", "DSA", "OOP",
        "DBMS", "Operating Systems", "Computer Networks", "Problem Solving"
    ]
    return [PlacementFundamental(name=name, proficiency=50) for name in default_names]


def load_user_data():
    """
    Load user profile from user_data.json.
    If missing or invalid, creates and returns default profile.
    """
    ensure_data_directory()
    if not os.path.exists(USER_DATA_FILE):
        # Create default profile
        roles = load_roles()
        default_role = roles[0] if roles else JobRole("data_analyst", "Data Analyst")
        profile = UserProfile(
            target_role=default_role.role_name,
            skills=default_role.default_skills,
            projects=[],
            fundamentals=get_default_fundamentals()
        )
        save_user_data(profile)
        return profile

    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return UserProfile.from_dict(data)
    except Exception as e:
        print(f"[Storage Error] Corrupted or invalid user_data.json: {e}")
        # Reset to default safely
        roles = load_roles()
        default_role = roles[0] if roles else JobRole("data_analyst", "Data Analyst")
        profile = UserProfile(
            target_role=default_role.role_name,
            skills=default_role.default_skills,
            projects=[],
            fundamentals=get_default_fundamentals()
        )
        save_user_data(profile)
        return profile


def save_user_data(user_profile):
    """
    Save UserProfile object to user_data.json.
    Returns True if successful, False otherwise.
    """
    ensure_data_directory()
    try:
        profile_dict = user_profile.to_dict() if isinstance(user_profile, UserProfile) else user_profile
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(profile_dict, f, indent=2)
        return True
    except Exception as e:
        print(f"[Storage Error] Failed to save user_data: {e}")
        return False
