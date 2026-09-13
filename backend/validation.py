"""
SkillTrack Backend Validation Module
Performs simple, explicit Core Python validation without regex or heavy dependencies.
"""


def validate_percentage(value, field_name="Percentage"):
    """
    Validate that percentage is an integer or float between 0 and 100.
    Returns (is_valid, error_message, cleaned_int_value)
    """
    if value is None:
        return False, f"{field_name} is required.", 0
    try:
        val = int(value)
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number.", 0

    if val < 0 or val > 100:
        return False, f"{field_name} must be between 0 and 100.", 0

    return True, "", val


def validate_skill(skill_name, existing_skills, is_new=True):
    """
    Validate skill creation or edit.
    """
    if not skill_name or not isinstance(skill_name, str) or not skill_name.strip():
        return False, "Skill name cannot be empty."

    clean_name = skill_name.strip()

    if is_new:
        for existing in existing_skills:
            ex_name = existing.name if hasattr(existing, 'name') else existing.get("name", "")
            if ex_name.lower() == clean_name.lower():
                return False, f"Skill '{clean_name}' already exists in your skill list."

    return True, ""


def validate_github_url(url):
    """
    Simple GitHub URL validation without regex.
    Must be a string containing 'github.com/' or starting with 'github.com'.
    """
    if not url or not isinstance(url, str) or not url.strip():
        return False, "GitHub Repository URL is mandatory."

    clean_url = url.strip().lower()

    if "github.com/" not in clean_url:
        return False, "Must be a valid GitHub Repository link (must contain 'github.com/')."

    return True, ""


def validate_project(project_data, current_projects, is_update=False):
    """
    Validate project creation or update.
    Strictly enforces maximum 5 projects.
    """
    proj_id = str(project_data.get("project_id", ""))
    name = project_data.get("name", "")
    github_url = project_data.get("github_url", "")

    if not name or not isinstance(name, str) or not name.strip():
        return False, "Project name is required."

    is_valid_gh, gh_err = validate_github_url(github_url)
    if not is_valid_gh:
        return False, gh_err

    # Check project limit
    if not is_update:
        if len(current_projects) >= 5:
            return False, "Maximum limit of 5 projects reached. Delete an existing project before adding a new one."
    else:
        # Check if project exists during update
        existing_ids = [str(p.project_id if hasattr(p, 'project_id') else p.get("project_id")) for p in current_projects]
        if proj_id not in existing_ids:
            return False, f"Project with ID '{proj_id}' does not exist."

    return True, ""
