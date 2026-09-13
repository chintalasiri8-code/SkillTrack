"""
SkillTrack Skill-Gap Analysis & Recommendation Engine
Rule-based analysis using Core Python logic to classify skills, calculate priorities,
and generate actionable career recommendations without external AI/ML libraries.
"""

from calculator import calculate_project_coverage, calculate_overall_job_readiness


def classify_skill(proficiency):
    """
    Categorize skill based on proficiency percentage:
    - 70-100: Strong
    - 40-69: Developing
    - 0-39: Weak
    """
    p = max(0, min(100, int(proficiency)))
    if p >= 70:
        return "Strong"
    elif p >= 40:
        return "Developing"
    else:
        return "Weak"


def calculate_skill_priority(proficiency, importance, is_demonstrated):
    """
    Calculate priority level for a skill based on:
    1. Proficiency percentage
    2. Role importance ("HIGH", "MEDIUM", "LOW")
    3. Project evidence (Boolean)

    Returns tuple: (priority_label, priority_rank_score)
    Priority labels: "VERY HIGH", "HIGH", "MEDIUM", "LOW"
    Rank score is an int (higher = higher priority for sorting).
    """
    prof = max(0, min(100, int(proficiency)))
    imp = importance.upper() if isinstance(importance, str) else "MEDIUM"

    if prof < 40 and imp == "HIGH" and not is_demonstrated:
        return "VERY HIGH", 4
    elif (prof < 40 and imp == "HIGH") or (prof < 60 and not is_demonstrated) or prof < 40:
        return "HIGH", 3
    elif (40 <= prof <= 69 and imp in ["HIGH", "MEDIUM"]) or (prof >= 70 and not is_demonstrated):
        return "MEDIUM", 2
    else:
        return "LOW", 1


def generate_skill_recommendation(skill_name, proficiency, importance, is_demonstrated):
    """
    Generate tailored recommendation string for an individual skill.
    """
    prof = max(0, min(100, int(proficiency)))

    if prof < 40 and not is_demonstrated:
        return f"Improve {skill_name} (currently {prof}%) and build a project demonstrating it."
    elif prof < 40 and is_demonstrated:
        return f"Your proficiency in {skill_name} is weak ({prof}%). Focus on core concepts to match your project evidence."
    elif 40 <= prof <= 69 and not is_demonstrated:
        return f"You have developing knowledge in {skill_name} ({prof}%). Build a project showcasing {skill_name} to prove your ability."
    elif 40 <= prof <= 69 and is_demonstrated:
        return f"Good progress in {skill_name} ({prof}%). Practice advanced problems to boost your proficiency above 70%."
    elif prof >= 70 and not is_demonstrated:
        return f"Strong theoretical proficiency in {skill_name} ({prof}%). Showcase this skill in an open-source GitHub project."
    else:
        return f"{skill_name} ({prof}%) is one of your key strengths with project evidence. Maintain your proficiency!"


def analyze_user_profile(user_profile):
    """
    Perform complete Skill Gap & Priority Analysis for a UserProfile.
    Returns structured analysis dict.
    """
    skills = user_profile.skills if hasattr(user_profile, 'skills') else user_profile.get("skills", [])
    projects = user_profile.projects if hasattr(user_profile, 'projects') else user_profile.get("projects", [])
    fundamentals = user_profile.fundamentals if hasattr(user_profile, 'fundamentals') else user_profile.get("fundamentals", [])

    coverage_info = calculate_project_coverage(skills, projects)
    demonstrated_names = set(name.lower() for name in coverage_info["demonstrated_skills"])

    strong_skills = []
    developing_skills = []
    weak_skills = []

    priority_skills = []

    for s in skills:
        name = s.name if hasattr(s, 'name') else s.get("name", "")
        prof = s.proficiency if hasattr(s, 'proficiency') else s.get("proficiency", 0)
        imp = s.importance if hasattr(s, 'importance') else s.get("importance", "MEDIUM")
        is_custom = s.is_custom if hasattr(s, 'is_custom') else s.get("is_custom", False)

        is_dem = name.strip().lower() in demonstrated_names
        category = classify_skill(prof)
        priority_label, rank_score = calculate_skill_priority(prof, imp, is_dem)
        recommendation = generate_skill_recommendation(name, prof, imp, is_dem)

        skill_analysis_item = {
            "name": name,
            "proficiency": prof,
            "importance": imp,
            "is_custom": is_custom,
            "is_demonstrated": is_dem,
            "category": category,
            "priority": priority_label,
            "priority_score": rank_score,
            "recommendation": recommendation
        }

        if category == "Strong":
            strong_skills.append(skill_analysis_item)
        elif category == "Developing":
            developing_skills.append(skill_analysis_item)
        else:
            weak_skills.append(skill_analysis_item)

        priority_skills.append(skill_analysis_item)

    # Sort priority skills by priority rank score descending, then by proficiency ascending
    priority_skills.sort(key=lambda item: (-item["priority_score"], item["proficiency"]))

    # Generate general profile recommendations
    overall_info = calculate_overall_job_readiness(user_profile)
    general_recommendations = []

    # Priority 1: Top skill gap action
    top_priority_items = [p for p in priority_skills if p["priority"] in ["VERY HIGH", "HIGH"]]
    if top_priority_items:
        top_skill = top_priority_items[0]
        general_recommendations.append(f"Focus on boosting {top_skill['name']} ({top_skill['proficiency']}%) as it is a high-priority gap.")

    # Priority 2: Project coverage action
    if len(projects) < 5:
        general_recommendations.append(f"Add more projects ({len(projects)}/5 complete). Ensure each project links to a valid GitHub repository.")
    if coverage_info["missing_skills"]:
        missing_sample = ", ".join(coverage_info["missing_skills"][:3])
        general_recommendations.append(f"Demonstrate missing skills in projects: {missing_sample}.")

    # Priority 3: Placement fundamentals action
    weak_fundamentals = [f for f in fundamentals if (f.proficiency if hasattr(f, 'proficiency') else f.get("proficiency", 0)) < 60]
    if weak_fundamentals:
        weak_names = ", ".join([f.name if hasattr(f, 'name') else f.get("name", "") for f in weak_fundamentals[:3]])
        general_recommendations.append(f"Improve placement fundamentals below 60%: {weak_names}.")

    if not general_recommendations:
        general_recommendations.append("Outstanding work! All tracked areas are in great shape. Keep building & refining projects.")

    return {
        "overall_summary": overall_info,
        "strong_skills": strong_skills,
        "developing_skills": developing_skills,
        "weak_skills": weak_skills,
        "priority_skills": priority_skills,
        "recommendations": general_recommendations
    }
