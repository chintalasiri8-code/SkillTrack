"""
SkillTrack Calculator Module
Performs numerical calculations for Skill, Project, Placement, and Overall Job Readiness.
Pure Core Python logic without external libraries.
"""


def calculate_skill_readiness(skills):
    """
    Calculate average proficiency across all target skills.
    Returns float (0 to 100).
    """
    if not skills:
        return 0.0
    
    total = sum(s.proficiency if hasattr(s, 'proficiency') else s.get("proficiency", 0) for s in skills)
    return float(total) / len(skills)


def calculate_project_coverage(required_skills, projects):
    """
    Calculate project skill coverage:
    Unique required skills demonstrated across all projects / Total required skills * 100
    Returns dict:
      - 'demonstrated_count': int
      - 'total_required': int
      - 'coverage_percentage': float
      - 'demonstrated_skills': list of skill names
      - 'missing_skills': list of skill names
    """
    if not required_skills:
        return {
            "demonstrated_count": 0,
            "total_required": 0,
            "coverage_percentage": 0.0,
            "demonstrated_skills": [],
            "missing_skills": []
        }

    # Extract all skill names demonstrated in any project
    demonstrated_in_projects = set()
    for proj in projects:
        skills_used = proj.skills_used if hasattr(proj, 'skills_used') else proj.get("skills_used", [])
        for s_name in skills_used:
            demonstrated_in_projects.add(s_name.strip().lower())

    required_names = [s.name if hasattr(s, 'name') else s.get("name", "") for s in required_skills]
    
    demonstrated_list = []
    missing_list = []

    for req_name in required_names:
        if req_name.strip().lower() in demonstrated_in_projects:
            demonstrated_list.append(req_name)
        else:
            missing_list.append(req_name)

    demonstrated_count = len(demonstrated_list)
    total_required = len(required_names)
    coverage_pct = (float(demonstrated_count) / total_required * 100.0) if total_required > 0 else 0.0

    return {
        "demonstrated_count": demonstrated_count,
        "total_required": total_required,
        "coverage_percentage": round(coverage_pct, 2),
        "demonstrated_skills": demonstrated_list,
        "missing_skills": missing_list
    }


def calculate_project_readiness(projects, required_skills):
    """
    Calculate Project Readiness based on:
    - Project Completion (20% weight): (count / 5) * 100
    - GitHub Evidence (20% weight): % of projects with valid GitHub link
    - Skill Coverage (60% weight): % of required skills covered across projects

    Returns dict with breakdown and overall float.
    """
    project_count = len(projects)
    
    # 1. Project Completion (max 5 projects = 100%)
    completion_pct = min(100.0, (float(project_count) / 5.0) * 100.0)

    # 2. GitHub Evidence
    github_valid_count = 0
    for p in projects:
        gh_url = p.github_url if hasattr(p, 'github_url') else p.get("github_url", "")
        if gh_url and "github.com/" in gh_url.lower():
            github_valid_count += 1
    
    github_evidence_pct = (float(github_valid_count) / project_count * 100.0) if project_count > 0 else 0.0

    # 3. Skill Coverage
    coverage_data = calculate_project_coverage(required_skills, projects)
    skill_coverage_pct = coverage_data["coverage_percentage"]

    # Final Project Readiness Formula
    project_readiness = (completion_pct * 0.20) + (github_evidence_pct * 0.20) + (skill_coverage_pct * 0.60)

    return {
        "project_count": project_count,
        "completion_pct": round(completion_pct, 1),
        "github_evidence_pct": round(github_evidence_pct, 1),
        "skill_coverage_pct": round(skill_coverage_pct, 1),
        "coverage_data": coverage_data,
        "project_readiness": round(project_readiness, 2)
    }


def calculate_placement_readiness(fundamentals):
    """
    Calculate average proficiency across all placement fundamentals.
    Returns float (0 to 100).
    """
    if not fundamentals:
        return 0.0

    total = sum(f.proficiency if hasattr(f, 'proficiency') else f.get("proficiency", 0) for f in fundamentals)
    return float(total) / len(fundamentals)


def calculate_overall_job_readiness(user_profile):
    """
    Calculate overall job readiness for a UserProfile object or dict:
    - Skill Readiness * 0.50
    - Project Readiness * 0.30
    - Placement Readiness * 0.20

    Returns comprehensive readiness summary dictionary.
    """
    skills = user_profile.skills if hasattr(user_profile, 'skills') else user_profile.get("skills", [])
    projects = user_profile.projects if hasattr(user_profile, 'projects') else user_profile.get("projects", [])
    fundamentals = user_profile.fundamentals if hasattr(user_profile, 'fundamentals') else user_profile.get("fundamentals", [])
    target_role = user_profile.target_role if hasattr(user_profile, 'target_role') else user_profile.get("target_role", "Data Analyst")

    skill_readiness = calculate_skill_readiness(skills)
    project_readiness_info = calculate_project_readiness(projects, skills)
    project_readiness = project_readiness_info["project_readiness"]
    placement_readiness = calculate_placement_readiness(fundamentals)

    overall_readiness = (skill_readiness * 0.50) + (project_readiness * 0.30) + (placement_readiness * 0.20)

    return {
        "target_role": target_role,
        "overall_readiness": round(overall_readiness),
        "overall_readiness_exact": round(overall_readiness, 2),
        "skill_readiness": round(skill_readiness),
        "skill_readiness_exact": round(skill_readiness, 2),
        "project_readiness": round(project_readiness),
        "project_readiness_exact": round(project_readiness, 2),
        "placement_readiness": round(placement_readiness),
        "placement_readiness_exact": round(placement_readiness, 2),
        "total_skills": len(skills),
        "total_projects": len(projects),
        "project_skill_coverage_str": f"{project_readiness_info['coverage_data']['demonstrated_count']} / {project_readiness_info['coverage_data']['total_required']}",
        "project_details": project_readiness_info
    }
