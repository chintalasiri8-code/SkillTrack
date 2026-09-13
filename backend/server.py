"""
SkillTrack Custom HTTP Server Handler
Extends BaseHTTPRequestHandler from Python's standard library.
Serves frontend static assets and exposes REST API endpoints.
Strictly no external frameworks (No Flask, Django, FastAPI, etc.).
"""

import json
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from models import UserProfile, Skill, Project, PlacementFundamental
from storage import load_roles, load_user_data, save_user_data
from calculator import calculate_overall_job_readiness
from analysis import analyze_user_profile
from validation import (
    validate_percentage,
    validate_skill,
    validate_project,
    validate_github_url
)

# Directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


class SkillTrackHTTPRequestHandler(BaseHTTPRequestHandler):
    """Custom HTTP Request Handler for SkillTrack."""

    def _set_headers(self, status_code=200, content_type="application/json"):
        """Send HTTP response status and headers with CORS support."""
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        """Handle preflight CORS requests."""
        self._set_headers(200, "text/plain")

    def _send_json(self, data, status_code=200):
        """Helper to send JSON response."""
        self._set_headers(status_code, "application/json")
        body = json.dumps(data, indent=2).encode("utf-8")
        self.wfile.write(body)

    def _send_error_json(self, error_message, status_code=400):
        """Helper to send error JSON response."""
        self._send_json({"success": False, "error": error_message}, status_code=status_code)

    def _parse_json_body(self):
        """Safely parse request JSON body."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                return {}
            body_bytes = self.rfile.read(content_length)
            return json.loads(body_bytes.decode("utf-8"))
        except Exception as e:
            print(f"[HTTP Request Error] Parsing JSON failed: {e}")
            return None

    # ==========================================
    # GET ROUTER
    # ==========================================
    def do_GET(self):
        """Handle GET requests for API endpoints and static assets."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # Handle API Endpoints
        if path.startswith("/api/"):
            if path == "/api/roles":
                roles = load_roles()
                self._send_json({"success": True, "roles": [r.to_dict() for r in roles]})
            
            elif path == "/api/user":
                profile = load_user_data()
                self._send_json({"success": True, "user": profile.to_dict()})

            elif path == "/api/readiness":
                profile = load_user_data()
                readiness_data = calculate_overall_job_readiness(profile)
                self._send_json({"success": True, "readiness": readiness_data})

            elif path == "/api/analysis":
                profile = load_user_data()
                analysis_data = analyze_user_profile(profile)
                self._send_json({"success": True, "analysis": analysis_data})

            elif path == "/api/skills":
                profile = load_user_data()
                self._send_json({"success": True, "skills": [s.to_dict() for s in profile.skills]})

            elif path == "/api/projects":
                profile = load_user_data()
                self._send_json({"success": True, "projects": [p.to_dict() for p in profile.projects]})

            elif path == "/api/fundamentals":
                profile = load_user_data()
                self._send_json({"success": True, "fundamentals": [f.to_dict() for f in profile.fundamentals]})

            else:
                self._send_error_json("API endpoint not found", 404)
            return

        # Serve static frontend files
        self._serve_static_file(path)

    # ==========================================
    # POST ROUTER
    # ==========================================
    def do_POST(self):
        """Handle POST requests for creating resources."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if not path.startswith("/api/"):
            self._send_error_json("Invalid route for POST", 404)
            return

        body = self._parse_json_body()
        if body is None:
            self._send_error_json("Invalid or missing JSON payload in request.", 400)
            return

        profile = load_user_data()

        # POST /api/user/role -> Select/change job role
        if path == "/api/user/role":
            role_name = body.get("role_name")
            if not role_name:
                self._send_error_json("role_name is required.", 400)
                return
            
            roles = load_roles()
            matched_role = next((r for r in roles if r.role_name.lower() == role_name.lower()), None)
            
            if not matched_role:
                self._send_error_json(f"Role '{role_name}' not found.", 404)
                return

            profile.target_role = matched_role.role_name
            # Retain custom skills if any, replace template skills with new role template skills
            existing_custom = [s for s in profile.skills if s.is_custom]
            profile.skills = list(matched_role.default_skills) + existing_custom

            save_user_data(profile)
            self._send_json({"success": True, "message": f"Role set to {matched_role.role_name}", "user": profile.to_dict()})

        # POST /api/skills -> Add custom skill
        elif path == "/api/skills":
            skill_name = body.get("name")
            proficiency = body.get("proficiency", 0)
            importance = body.get("importance", "MEDIUM")

            is_valid, err_msg = validate_skill(skill_name, profile.skills, is_new=True)
            if not is_valid:
                self._send_error_json(err_msg, 400)
                return

            is_valid_p, p_err, p_val = validate_percentage(proficiency, "Proficiency")
            if not is_valid_p:
                self._send_error_json(p_err, 400)
                return

            new_skill = Skill(name=skill_name.strip(), proficiency=p_val, importance=importance, is_custom=True)
            profile.skills.append(new_skill)
            save_user_data(profile)
            self._send_json({"success": True, "message": f"Custom skill '{new_skill.name}' added successfully.", "skill": new_skill.to_dict(), "skills": [s.to_dict() for s in profile.skills]}, 201)

        # POST /api/projects -> Add project (Max 5 enforced!)
        elif path == "/api/projects":
            is_valid_proj, proj_err = validate_project(body, profile.projects, is_update=False)
            if not is_valid_proj:
                self._send_error_json(proj_err, 400)
                return

            new_id = str(len(profile.projects) + 1)
            # Ensure unique ID if any deleted previously
            existing_ids = set(p.project_id for p in profile.projects)
            counter = 1
            while str(counter) in existing_ids:
                counter += 1
            new_id = str(counter)

            new_project = Project(
                project_id=new_id,
                name=body.get("name", "").strip(),
                github_url=body.get("github_url", "").strip(),
                description=body.get("description", "").strip(),
                skills_used=body.get("skills_used", []),
                topics_covered=body.get("topics_covered", [])
            )
            profile.projects.append(new_project)
            save_user_data(profile)
            self._send_json({"success": True, "message": "Project added successfully.", "project": new_project.to_dict(), "projects": [p.to_dict() for p in profile.projects]}, 201)

        else:
            self._send_error_json("Endpoint not found", 404)

    # ==========================================
    # PUT ROUTER
    # ==========================================
    def do_PUT(self):
        """Handle PUT requests for updating existing resources."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if not path.startswith("/api/"):
            self._send_error_json("Invalid route for PUT", 404)
            return

        body = self._parse_json_body()
        if body is None:
            self._send_error_json("Invalid or missing JSON payload.", 400)
            return

        profile = load_user_data()

        # PUT /api/skills -> Update skill proficiencies
        if path == "/api/skills":
            skills_payload = body.get("skills")
            if not isinstance(skills_payload, list):
                self._send_error_json("'skills' array is required in body.", 400)
                return

            updated_map = {item.get("name", "").strip().lower(): item.get("proficiency") for item in skills_payload if isinstance(item, dict)}

            for s in profile.skills:
                key = s.name.strip().lower()
                if key in updated_map:
                    is_valid_p, p_err, p_val = validate_percentage(updated_map[key], f"Proficiency for {s.name}")
                    if is_valid_p:
                        s.proficiency = p_val

            save_user_data(profile)
            self._send_json({"success": True, "message": "Skill proficiencies updated.", "skills": [s.to_dict() for s in profile.skills]})

        # PUT /api/projects -> Update project
        elif path == "/api/projects":
            proj_id = str(body.get("project_id", ""))
            is_valid_proj, proj_err = validate_project(body, profile.projects, is_update=True)
            if not is_valid_proj:
                self._send_error_json(proj_err, 400)
                return

            target_proj = next((p for p in profile.projects if p.project_id == proj_id), None)
            if not target_proj:
                self._send_error_json(f"Project with ID '{proj_id}' not found.", 404)
                return

            target_proj.name = body.get("name", target_proj.name).strip()
            target_proj.github_url = body.get("github_url", target_proj.github_url).strip()
            target_proj.description = body.get("description", target_proj.description).strip()
            target_proj.skills_used = body.get("skills_used", target_proj.skills_used)
            target_proj.topics_covered = body.get("topics_covered", target_proj.topics_covered)

            save_user_data(profile)
            self._send_json({"success": True, "message": "Project updated successfully.", "project": target_proj.to_dict(), "projects": [p.to_dict() for p in profile.projects]})

        # PUT /api/fundamentals -> Update placement fundamentals
        elif path == "/api/fundamentals":
            fundamentals_payload = body.get("fundamentals")
            if not isinstance(fundamentals_payload, list):
                self._send_error_json("'fundamentals' array is required.", 400)
                return

            updated_map = {item.get("name", "").strip().lower(): item.get("proficiency") for item in fundamentals_payload if isinstance(item, dict)}

            for f in profile.fundamentals:
                key = f.name.strip().lower()
                if key in updated_map:
                    is_valid_p, p_err, p_val = validate_percentage(updated_map[key], f"Proficiency for {f.name}")
                    if is_valid_p:
                        f.proficiency = p_val

            save_user_data(profile)
            self._send_json({"success": True, "message": "Placement fundamentals updated.", "fundamentals": [f.to_dict() for f in profile.fundamentals]})

        else:
            self._send_error_json("Endpoint not found", 404)

    # ==========================================
    # DELETE ROUTER
    # ==========================================
    def do_DELETE(self):
        """Handle DELETE requests for removing resources."""
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if not path.startswith("/api/"):
            self._send_error_json("Invalid route for DELETE", 404)
            return

        profile = load_user_data()
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # DELETE /api/projects?id=1
        if path == "/api/projects":
            proj_id_list = query_params.get("id")
            if not proj_id_list:
                # Check JSON body fallback
                body = self._parse_json_body()
                proj_id = str(body.get("project_id", "")) if body else ""
            else:
                proj_id = str(proj_id_list[0])

            if not proj_id:
                self._send_error_json("project_id query param or JSON body is required.", 400)
                return

            initial_count = len(profile.projects)
            profile.projects = [p for p in profile.projects if p.project_id != proj_id]

            if len(profile.projects) == initial_count:
                self._send_error_json(f"Project with ID '{proj_id}' not found.", 404)
                return

            save_user_data(profile)
            self._send_json({"success": True, "message": f"Project '{proj_id}' deleted.", "projects": [p.to_dict() for p in profile.projects]})

        # DELETE /api/skills?name=TypeScript
        elif path == "/api/skills":
            skill_name_list = query_params.get("name")
            if not skill_name_list:
                body = self._parse_json_body()
                skill_name = str(body.get("name", "")) if body else ""
            else:
                skill_name = str(skill_name_list[0])

            if not skill_name:
                self._send_error_json("Skill name query param or JSON body is required.", 400)
                return

            initial_count = len(profile.skills)
            profile.skills = [s for s in profile.skills if s.name.strip().lower() != skill_name.strip().lower()]

            if len(profile.skills) == initial_count:
                self._send_error_json(f"Skill '{skill_name}' not found.", 404)
                return

            save_user_data(profile)
            self._send_json({"success": True, "message": f"Skill '{skill_name}' removed.", "skills": [s.to_dict() for s in profile.skills]})

        else:
            self._send_error_json("Endpoint not found", 404)

    # ==========================================
    # STATIC FILE SERVING
    # ==========================================
    def _serve_static_file(self, req_path):
        """Serve static files from frontend directory."""
        if req_path == "/" or req_path == "/index.html":
            file_path = os.path.join(FRONTEND_DIR, "index.html")
        else:
            # Strip leading slash
            rel_path = req_path.lstrip("/").replace("/", os.sep)
            file_path = os.path.join(FRONTEND_DIR, rel_path)

        # Prevent directory traversal attacks
        real_file_path = os.path.realpath(file_path)
        real_frontend_dir = os.path.realpath(FRONTEND_DIR)

        if not real_file_path.startswith(real_frontend_dir):
            self._send_error_json("Forbidden", 403)
            return

        if not os.path.exists(real_file_path) or os.path.isdir(real_file_path):
            # Fallback to index.html for SPA router behavior
            file_path = os.path.join(FRONTEND_DIR, "index.html")

        # Determine MIME Content-Type
        content_type = "text/html"
        if file_path.endswith(".css"):
            content_type = "text/css"
        elif file_path.endswith(".js"):
            content_type = "application/javascript"
        elif file_path.endswith(".json"):
            content_type = "application/json"
        elif file_path.endswith(".png"):
            content_type = "image/png"
        elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            content_type = "image/jpeg"
        elif file_path.endswith(".svg"):
            content_type = "image/svg+xml"
        elif file_path.endswith(".ico"):
            content_type = "image/x-icon"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self._set_headers(200, content_type)
            self.wfile.write(content)
        except Exception as e:
            print(f"[Static Serve Error] {e}")
            self._send_error_json("Internal server error serving static file", 500)
