/**
 * SkillTrack - Frontend JavaScript Logic
 * Interacts with Python BaseHTTPRequestHandler API endpoints via fetch()
 * All business logic & calculations are computed strictly on the Core Python backend.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Global State Cache
  let currentProfile = null;
  let availableRoles = [];
  let currentReadiness = null;
  let currentAnalysis = null;

  // DOM Elements
  const header = document.getElementById("main-header");
  const navButtons = document.querySelectorAll(".nav-btn");
  const viewSections = document.querySelectorAll(".view-section");
  const navLogo = document.getElementById("nav-logo");
  const headerRoleBadge = document.getElementById("header-target-role");
  const toastContainer = document.getElementById("toast-container");

  // Landing
  const btnGetStarted = document.getElementById("btn-get-started");

  // Dashboard
  const dashRoleName = document.getElementById("dash-role-name");
  const dashChangeRoleBtn = document.getElementById("dash-change-role-btn");
  const overallGaugeRing = document.getElementById("overall-gauge-ring");
  const overallScoreVal = document.getElementById("overall-score-val");
  const dashValSkill = document.getElementById("dash-val-skill");
  const dashBarSkill = document.getElementById("dash-bar-skill");
  const dashValProject = document.getElementById("dash-val-project");
  const dashBarProject = document.getElementById("dash-bar-project");
  const dashValPlacement = document.getElementById("dash-val-placement");
  const dashBarPlacement = document.getElementById("dash-bar-placement");
  const dashStatSkillsCount = document.getElementById("dash-stat-skills-count");
  const dashStatProjectsCount = document.getElementById("dash-stat-projects-count");
  const dashStatCoverageStr = document.getElementById("dash-stat-coverage-str");
  const dashPrioritiesList = document.getElementById("dash-priorities-list");
  const dashCountStrong = document.getElementById("dash-count-strong");
  const dashCountDeveloping = document.getElementById("dash-count-developing");
  const dashCountWeak = document.getElementById("dash-count-weak");
  const dashSkillsPreviewList = document.getElementById("dash-skills-preview-list");

  // Skills View
  const roleSelect = document.getElementById("role-select");
  const btnApplyRole = document.getElementById("btn-apply-role");
  const btnOpenCustomSkillModal = document.getElementById("btn-open-custom-skill-modal");
  const btnSaveSkills = document.getElementById("btn-save-skills");
  const skillsCountBadge = document.getElementById("skills-count-badge");
  const skillsListContainer = document.getElementById("skills-list-container");

  // Projects View
  const btnOpenProjectModal = document.getElementById("btn-open-project-modal");
  const projCounterBadge = document.getElementById("proj-counter-badge");
  const projCoveragePct = document.getElementById("proj-coverage-pct");
  const projCoverageSub = document.getElementById("proj-coverage-sub");
  const projCoverageFill = document.getElementById("proj-coverage-fill");
  const projDemonstratedTags = document.getElementById("proj-demonstrated-tags");
  const projectsGrid = document.getElementById("projects-grid");

  // Placement View
  const placementOverallVal = document.getElementById("placement-overall-val");
  const fundamentalsEditorGrid = document.getElementById("fundamentals-editor-grid");
  const btnSaveFundamentals = document.getElementById("btn-save-fundamentals");

  // Analysis View
  const analysisGeneralRecs = document.getElementById("analysis-general-recs");
  const analysisPriorityList = document.getElementById("analysis-priority-list");
  const analysisStrongList = document.getElementById("analysis-strong-list");
  const analysisDevelopingList = document.getElementById("analysis-developing-list");
  const analysisWeakList = document.getElementById("analysis-weak-list");

  // Modals
  const modalAddSkill = document.getElementById("modal-add-skill");
  const formAddSkill = document.getElementById("form-add-skill");

  const modalProject = document.getElementById("modal-project");
  const modalProjectTitle = document.getElementById("modal-project-title");
  const formProject = document.getElementById("form-project");
  const inputProjId = document.getElementById("input-proj-id");
  const inputProjName = document.getElementById("input-proj-name");
  const inputProjGithub = document.getElementById("input-proj-github");
  const inputProjDesc = document.getElementById("input-proj-desc");
  const modalProjSkillsCheckboxes = document.getElementById("modal-proj-skills-checkboxes");
  const inputProjTopics = document.getElementById("input-proj-topics");

  // Initialize App
  init();

  async function init() {
    setupEventListeners();
    await fetchRoles();
    await fetchUserData();
    await refreshAllData();
  }

  // Toast Notification System
  function showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${type === "success" ? "✓" : "⚠️"}</span> <span>${message}</span>`;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 4000);
  }

  // Navigation Handling
  function switchView(viewName) {
    if (viewName === "landing") {
      header.classList.add("hidden");
    } else {
      header.classList.remove("hidden");
    }

    viewSections.forEach((sec) => {
      if (sec.id === `view-${viewName}`) {
        sec.classList.remove("hidden");
        sec.classList.add("active");
      } else {
        sec.classList.add("hidden");
        sec.classList.remove("active");
      }
    });

    navButtons.forEach((btn) => {
      if (btn.dataset.view === viewName) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function setupEventListeners() {
    // Navigation
    btnGetStarted.addEventListener("click", () => switchView("dashboard"));
    navLogo.addEventListener("click", () => switchView("landing"));

    navButtons.forEach((btn) => {
      btn.addEventListener("click", () => switchView(btn.dataset.view));
    });

    document.querySelectorAll("[data-view]").forEach((el) => {
      el.addEventListener("click", (e) => {
        const targetView = e.currentTarget.dataset.view;
        if (targetView) switchView(targetView);
      });
    });

    // Dash Action
    dashChangeRoleBtn.addEventListener("click", () => switchView("skills"));

    // Modal Close Triggers
    document.querySelectorAll(".modal-close").forEach((btn) => {
      btn.addEventListener("click", () => {
        const modalId = btn.dataset.modal;
        if (modalId) {
          document.getElementById(modalId).classList.add("hidden");
        }
      });
    });

    // Custom Skill Modal
    btnOpenCustomSkillModal.addEventListener("click", () => {
      formAddSkill.reset();
      modalAddSkill.classList.remove("hidden");
    });

    formAddSkill.addEventListener("submit", handleAddCustomSkill);

    // Save Skills
    btnSaveSkills.addEventListener("click", handleSaveSkills);

    // Switch Role
    btnApplyRole.addEventListener("click", handleSwitchRole);

    // Project Modal
    btnOpenProjectModal.addEventListener("click", () => openProjectModal());
    formProject.addEventListener("submit", handleSaveProject);

    // Save Fundamentals
    btnSaveFundamentals.addEventListener("click", handleSaveFundamentals);
  }

  // ==========================================
  // API FETCHERS
  // ==========================================
  async function fetchRoles() {
    try {
      const res = await fetch("/api/roles");
      const data = await res.json();
      if (data.success) {
        availableRoles = data.roles;
        renderRoleOptions();
      }
    } catch (e) {
      console.error("Failed to fetch roles:", e);
    }
  }

  async function fetchUserData() {
    try {
      const res = await fetch("/api/user");
      const data = await res.json();
      if (data.success) {
        currentProfile = data.user;
        headerRoleBadge.textContent = currentProfile.target_role;
        dashRoleName.textContent = currentProfile.target_role;
      }
    } catch (e) {
      console.error("Failed to fetch user data:", e);
    }
  }

  async function refreshAllData() {
    try {
      // 1. Fetch User Data
      await fetchUserData();

      // 2. Fetch Readiness
      const resReadiness = await fetch("/api/readiness");
      const dataReadiness = await resReadiness.json();
      if (dataReadiness.success) {
        currentReadiness = dataReadiness.readiness;
      }

      // 3. Fetch Analysis
      const resAnalysis = await fetch("/api/analysis");
      const dataAnalysis = await resAnalysis.json();
      if (dataAnalysis.success) {
        currentAnalysis = dataAnalysis.analysis;
      }

      // Render Views
      renderDashboard();
      renderSkillsEditor();
      renderProjectsView();
      renderFundamentalsEditor();
      renderAnalysisView();

    } catch (e) {
      console.error("Error refreshing data:", e);
    }
  }

  // ==========================================
  // DASHBOARD RENDERER
  // ==========================================
  function renderDashboard() {
    if (!currentReadiness || !currentAnalysis) return;

    const overall = currentReadiness.overall_readiness;
    overallGaugeRing.style.setProperty("--score-pct", `${overall}%`);
    overallScoreVal.textContent = `${overall}%`;

    dashValSkill.textContent = `${currentReadiness.skill_readiness}%`;
    dashBarSkill.style.width = `${currentReadiness.skill_readiness}%`;

    dashValProject.textContent = `${currentReadiness.project_readiness}%`;
    dashBarProject.style.width = `${currentReadiness.project_readiness}%`;

    dashValPlacement.textContent = `${currentReadiness.placement_readiness}%`;
    dashBarPlacement.style.width = `${currentReadiness.placement_readiness}%`;

    dashStatSkillsCount.textContent = currentReadiness.total_skills;
    dashStatProjectsCount.textContent = `${currentReadiness.total_projects} / 5`;
    dashStatCoverageStr.textContent = currentReadiness.project_skill_coverage_str;

    // Skill Counts
    dashCountStrong.textContent = currentAnalysis.strong_skills.length;
    dashCountDeveloping.textContent = currentAnalysis.developing_skills.length;
    dashCountWeak.textContent = currentAnalysis.weak_skills.length;

    // Render Priorities (Top 3)
    dashPrioritiesList.innerHTML = "";
    const topPriorities = currentAnalysis.priority_skills.slice(0, 3);

    if (topPriorities.length === 0) {
      dashPrioritiesList.innerHTML = `<li class="priority-item"><div class="priority-content"><p>No high-priority skill gaps identified!</p></div></li>`;
    } else {
      topPriorities.forEach((p) => {
        const li = document.createElement("li");
        li.className = "priority-item";
        const tagClass = p.priority.toLowerCase().replace(" ", "-");

        li.innerHTML = `
          <span class="priority-tag ${tagClass}">${p.priority}</span>
          <div class="priority-content">
            <strong>${p.name} (${p.proficiency}%)</strong>
            <p>${p.recommendation}</p>
          </div>
        `;
        dashPrioritiesList.appendChild(li);
      });
    }

    // Render Skills Preview List (Top 5)
    dashSkillsPreviewList.innerHTML = "";
    currentProfile.skills.slice(0, 5).forEach((s) => {
      const div = document.createElement("div");
      div.className = "skill-preview-row";
      let catClass = s.proficiency >= 70 ? "text-strong" : s.proficiency >= 40 ? "text-developing" : "text-weak";

      div.innerHTML = `
        <span>${s.name}</span>
        <span class="${catClass} font-bold">${s.proficiency}%</span>
      `;
      dashSkillsPreviewList.appendChild(div);
    });
  }

  // ==========================================
  // SKILLS EDITOR RENDERER
  // ==========================================
  function renderRoleOptions() {
    roleSelect.innerHTML = "";
    availableRoles.forEach((r) => {
      const opt = document.createElement("option");
      opt.value = r.role_name;
      opt.textContent = r.role_name;
      if (currentProfile && currentProfile.target_role === r.role_name) {
        opt.selected = true;
      }
      roleSelect.appendChild(opt);
    });
  }

  function renderSkillsEditor() {
    if (!currentProfile) return;

    skillsCountBadge.textContent = currentProfile.skills.length;
    skillsListContainer.innerHTML = "";

    // Set select value
    if (roleSelect.querySelector(`option[value="${currentProfile.target_role}"]`)) {
      roleSelect.value = currentProfile.target_role;
    }

    currentProfile.skills.forEach((s) => {
      const card = document.createElement("div");
      card.className = "skill-card";

      let catClass = "badge-weak";
      let catText = "Weak";
      if (s.proficiency >= 70) { catClass = "badge-strong"; catText = "Strong"; }
      else if (s.proficiency >= 40) { catClass = "badge-developing"; catText = "Developing"; }

      const isDem = currentAnalysis && currentAnalysis.priority_skills.some((ps) => ps.name.toLowerCase() === s.name.toLowerCase() && ps.is_demonstrated);

      card.innerHTML = `
        <div class="skill-card-top">
          <span class="skill-name">${s.name}</span>
          <div class="skill-badges">
            <span class="badge ${catClass}">${catText}</span>
            <span class="badge badge-outline" style="border: 1px solid var(--bg-card-border); color: var(--text-muted);">${s.importance}</span>
            ${s.is_custom ? `<span class="badge badge-custom">Custom</span>` : ''}
            ${isDem ? `<span class="badge badge-evidence">✓ Project Evidence</span>` : ''}
          </div>
        </div>

        <div class="skill-slider-box">
          <input type="range" class="range-slider skill-range-input" data-skill="${s.name}" min="0" max="100" value="${s.proficiency}">
          <input type="number" class="form-control skill-pct-input" data-skill="${s.name}" min="0" max="100" value="${s.proficiency}">
          ${s.is_custom ? `<button class="btn-danger-sm btn-delete-skill" data-skill="${s.name}">Delete</button>` : ''}
        </div>
      `;

      skillsListContainer.appendChild(card);
    });

    // Synchronize slider and number input
    skillsListContainer.querySelectorAll(".skill-range-input").forEach((slider) => {
      slider.addEventListener("input", (e) => {
        const sName = e.target.dataset.skill;
        const numInput = skillsListContainer.querySelector(`.skill-pct-input[data-skill="${CSS.escape(sName)}"]`);
        if (numInput) numInput.value = e.target.value;
      });
    });

    skillsListContainer.querySelectorAll(".skill-pct-input").forEach((numInput) => {
      numInput.addEventListener("input", (e) => {
        const sName = e.target.dataset.skill;
        const slider = skillsListContainer.querySelector(`.skill-range-input[data-skill="${CSS.escape(sName)}"]`);
        if (slider) slider.value = e.target.value;
      });
    });

    // Delete custom skill buttons
    skillsListContainer.querySelectorAll(".btn-delete-skill").forEach((btn) => {
      btn.addEventListener("click", () => handleDeleteCustomSkill(btn.dataset.skill));
    });
  }

  async function handleSwitchRole() {
    const selectedRole = roleSelect.value;
    try {
      const res = await fetch("/api/user/role", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role_name: selectedRole })
      });
      const data = await res.json();
      if (data.success) {
        showToast(`Role switched to ${selectedRole}`);
        await refreshAllData();
      } else {
        showToast(data.error || "Failed to switch role", "error");
      }
    } catch (e) {
      showToast("Server error switching role", "error");
    }
  }

  async function handleAddCustomSkill(e) {
    e.preventDefault();
    const name = document.getElementById("input-skill-name").value.trim();
    const prof = parseInt(document.getElementById("input-skill-prof").value, 10);
    const imp = document.getElementById("input-skill-imp").value;

    try {
      const res = await fetch("/api/skills", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, proficiency: prof, importance: imp })
      });
      const data = await res.json();
      if (data.success) {
        showToast(`Skill '${name}' added successfully!`);
        modalAddSkill.classList.add("hidden");
        await refreshAllData();
      } else {
        showToast(data.error || "Failed to add skill", "error");
      }
    } catch (e) {
      showToast("Server error adding skill", "error");
    }
  }

  async function handleSaveSkills() {
    const updatedSkills = [];
    skillsListContainer.querySelectorAll(".skill-pct-input").forEach((input) => {
      updatedSkills.push({
        name: input.dataset.skill,
        proficiency: parseInt(input.value, 10) || 0
      });
    });

    try {
      const res = await fetch("/api/skills", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ skills: updatedSkills })
      });
      const data = await res.json();
      if (data.success) {
        showToast("Skill proficiencies saved!");
        await refreshAllData();
      } else {
        showToast(data.error || "Failed to save skills", "error");
      }
    } catch (e) {
      showToast("Server error saving skills", "error");
    }
  }

  async function handleDeleteCustomSkill(skillName) {
    if (!confirm(`Are you sure you want to remove '${skillName}'?`)) return;
    try {
      const res = await fetch(`/api/skills?name=${encodeURIComponent(skillName)}`, {
        method: "DELETE"
      });
      const data = await res.json();
      if (data.success) {
        showToast(`Skill '${skillName}' removed.`);
        await refreshAllData();
      } else {
        showToast(data.error || "Failed to remove skill", "error");
      }
    } catch (e) {
      showToast("Server error deleting skill", "error");
    }
  }

  // ==========================================
  // PROJECTS VIEW RENDERER
  // ==========================================
  function renderProjectsView() {
    if (!currentProfile || !currentReadiness) return;

    const count = currentProfile.projects.length;
    projCounterBadge.textContent = `${count}/5`;

    // Enforce 5 projects maximum on button
    if (count >= 5) {
      btnOpenProjectModal.disabled = true;
      btnOpenProjectModal.style.opacity = "0.5";
      btnOpenProjectModal.title = "Maximum limit of 5 projects reached";
    } else {
      btnOpenProjectModal.disabled = false;
      btnOpenProjectModal.style.opacity = "1";
      btnOpenProjectModal.title = "";
    }

    const projInfo = currentReadiness.project_details;
    const covData = projInfo.coverage_data;

    projCoveragePct.textContent = `${covData.coverage_percentage}%`;
    projCoverageSub.textContent = `Demonstrated ${covData.demonstrated_count} of ${covData.total_required} required target skills.`;
    projCoverageFill.style.width = `${covData.coverage_percentage}%`;

    // Demonstrated Skill Tags
    projDemonstratedTags.innerHTML = "";
    currentProfile.skills.forEach((s) => {
      const isDem = covData.demonstrated_skills.some((ds) => ds.toLowerCase() === s.name.toLowerCase());
      const tag = document.createElement("span");
      tag.className = `skill-tag ${isDem ? "covered" : ""}`;
      tag.textContent = `${isDem ? "✓ " : ""}${s.name}`;
      projDemonstratedTags.appendChild(tag);
    });

    // Render Projects Grid
    projectsGrid.innerHTML = "";
    if (currentProfile.projects.length === 0) {
      projectsGrid.innerHTML = `
        <div class="glass-card" style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
          <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 1rem;">No projects added yet.</p>
          <p style="font-size: 0.9rem; color: var(--text-dim);">Add up to 5 projects with GitHub repository links to build your project readiness score.</p>
        </div>
      `;
      return;
    }

    currentProfile.projects.forEach((p) => {
      const card = document.createElement("div");
      card.className = "project-card";

      const skillsTags = p.skills_used.map((sk) => `<span class="skill-tag covered">${sk}</span>`).join(" ");
      const topicsTags = p.topics_covered.map((tp) => `<span class="skill-tag">${tp}</span>`).join(" ");

      card.innerHTML = `
        <div>
          <div class="project-title-row">
            <h4 class="project-title">${p.name}</h4>
          </div>

          <a href="${p.github_url}" target="_blank" rel="noopener" class="github-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
            ${p.github_url}
          </a>

          <p class="project-desc">${p.description || "No description provided."}</p>

          <div style="margin-bottom: 0.75rem;">
            <div class="project-meta-label">Skills Demonstrated</div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.4rem;">${skillsTags || '<span style="color: var(--text-dim); font-size: 0.8rem;">None selected</span>'}</div>
          </div>

          <div>
            <div class="project-meta-label">Topics Covered</div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.4rem;">${topicsTags || '<span style="color: var(--text-dim); font-size: 0.8rem;">None</span>'}</div>
          </div>
        </div>

        <div class="project-card-actions">
          <button class="btn btn-outline btn-edit-proj" data-id="${p.project_id}">Edit</button>
          <button class="btn-danger-sm btn-delete-proj" data-id="${p.project_id}">Delete</button>
        </div>
      `;

      projectsGrid.appendChild(card);
    });

    // Attach project button listeners
    projectsGrid.querySelectorAll(".btn-edit-proj").forEach((btn) => {
      btn.addEventListener("click", () => openProjectModal(btn.dataset.id));
    });

    projectsGrid.querySelectorAll(".btn-delete-proj").forEach((btn) => {
      btn.addEventListener("click", () => handleDeleteProject(btn.dataset.id));
    });
  }

  function openProjectModal(projectId = null) {
    formProject.reset();
    modalProjSkillsCheckboxes.innerHTML = "";

    // Build skill checkboxes
    currentProfile.skills.forEach((s) => {
      const label = document.createElement("label");
      label.className = "checkbox-item";
      label.innerHTML = `
        <input type="checkbox" name="skills_used" value="${s.name}">
        <span>${s.name}</span>
      `;
      modalProjSkillsCheckboxes.appendChild(label);
    });

    if (projectId) {
      modalProjectTitle.textContent = "Edit Project";
      const targetProj = currentProfile.projects.find((p) => p.project_id === projectId);
      if (targetProj) {
        inputProjId.value = targetProj.project_id;
        inputProjName.value = targetProj.name;
        inputProjGithub.value = targetProj.github_url;
        inputProjDesc.value = targetProj.description || "";
        inputProjTopics.value = targetProj.topics_covered ? targetProj.topics_covered.join(", ") : "";

        // Check skills
        modalProjSkillsCheckboxes.querySelectorAll("input[type='checkbox']").forEach((cb) => {
          if (targetProj.skills_used.includes(cb.value)) {
            cb.checked = true;
          }
        });
      }
    } else {
      modalProjectTitle.textContent = "Add Project";
      inputProjId.value = "";
    }

    modalProject.classList.remove("hidden");
  }

  async function handleSaveProject(e) {
    e.preventDefault();

    const projId = inputProjId.value;
    const name = inputProjName.value.trim();
    const github_url = inputProjGithub.value.trim();
    const description = inputProjDesc.value.trim();
    const topics_raw = inputProjTopics.value.trim();

    const selectedSkills = [];
    modalProjSkillsCheckboxes.querySelectorAll("input[type='checkbox']:checked").forEach((cb) => {
      selectedSkills.push(cb.value);
    });

    const topics = topics_raw ? topics_raw.split(",").map((t) => t.trim()).filter((t) => t.length > 0) : [];

    const payload = {
      project_id: projId,
      name,
      github_url,
      description,
      skills_used: selectedSkills,
      topics_covered: topics
    };

    try {
      const method = projId ? "PUT" : "POST";
      const res = await fetch("/api/projects", {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message || "Project saved successfully!");
        modalProject.classList.add("hidden");
        await refreshAllData();
      } else {
        showToast(data.error || "Failed to save project", "error");
      }
    } catch (e) {
      showToast("Server error saving project", "error");
    }
  }

  async function handleDeleteProject(projId) {
    if (!confirm("Are you sure you want to delete this project?")) return;
    try {
      const res = await fetch(`/api/projects?id=${encodeURIComponent(projId)}`, {
        method: "DELETE"
      });
      const data = await res.json();
      if (data.success) {
        showToast("Project deleted.");
        await refreshAllData();
      } else {
        showToast(data.error || "Failed to delete project", "error");
      }
    } catch (e) {
      showToast("Server error deleting project", "error");
    }
  }

  // ==========================================
  // PLACEMENT FUNDAMENTALS RENDERER
  // ==========================================
  function renderFundamentalsEditor() {
    if (!currentProfile || !currentReadiness) return;

    placementOverallVal.textContent = `${currentReadiness.placement_readiness}%`;
    fundamentalsEditorGrid.innerHTML = "";

    currentProfile.fundamentals.forEach((f) => {
      const card = document.createElement("div");
      card.className = "fundamental-item-card";

      card.innerHTML = `
        <div class="skill-card-top">
          <span class="skill-name">${f.name}</span>
          <span class="badge ${f.proficiency >= 70 ? "badge-strong" : f.proficiency >= 40 ? "badge-developing" : "badge-weak"}">
            ${f.proficiency}%
          </span>
        </div>

        <div class="skill-slider-box">
          <input type="range" class="range-slider fund-range-input" data-fund="${f.name}" min="0" max="100" value="${f.proficiency}">
          <input type="number" class="form-control fund-pct-input" data-fund="${f.name}" min="0" max="100" value="${f.proficiency}">
        </div>
      `;

      fundamentalsEditorGrid.appendChild(card);
    });

    // Synchronize inputs
    fundamentalsEditorGrid.querySelectorAll(".fund-range-input").forEach((slider) => {
      slider.addEventListener("input", (e) => {
        const fName = e.target.dataset.fund;
        const numInput = fundamentalsEditorGrid.querySelector(`.fund-pct-input[data-fund="${CSS.escape(fName)}"]`);
        if (numInput) numInput.value = e.target.value;
      });
    });

    fundamentalsEditorGrid.querySelectorAll(".fund-pct-input").forEach((numInput) => {
      numInput.addEventListener("input", (e) => {
        const fName = e.target.dataset.fund;
        const slider = fundamentalsEditorGrid.querySelector(`.fund-range-input[data-fund="${CSS.escape(fName)}"]`);
        if (slider) slider.value = e.target.value;
      });
    });
  }

  async function handleSaveFundamentals() {
    const updatedFunds = [];
    fundamentalsEditorGrid.querySelectorAll(".fund-pct-input").forEach((input) => {
      updatedFunds.push({
        name: input.dataset.fund,
        proficiency: parseInt(input.value, 10) || 0
      });
    });

    try {
      const res = await fetch("/api/fundamentals", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fundamentals: updatedFunds })
      });
      const data = await res.json();
      if (data.success) {
        showToast("Placement fundamentals saved!");
        await refreshAllData();
      } else {
        showToast(data.error || "Failed to save fundamentals", "error");
      }
    } catch (e) {
      showToast("Server error saving fundamentals", "error");
    }
  }

  // ==========================================
  // GAP ANALYSIS RENDERER
  // ==========================================
  function renderAnalysisView() {
    if (!currentAnalysis) return;

    // General Recommendations List
    analysisGeneralRecs.innerHTML = "";
    currentAnalysis.recommendations.forEach((rec) => {
      const li = document.createElement("li");
      li.innerHTML = `<span>🎯</span> <span>${rec}</span>`;
      analysisGeneralRecs.appendChild(li);
    });

    // Priority Skills List
    analysisPriorityList.innerHTML = "";
    currentAnalysis.priority_skills.forEach((ps) => {
      const card = document.createElement("div");
      card.className = "priority-item";
      const tagClass = ps.priority.toLowerCase().replace(" ", "-");

      card.innerHTML = `
        <span class="priority-tag ${tagClass}">${ps.priority}</span>
        <div class="priority-content">
          <strong>${ps.name} (${ps.proficiency}%)</strong>
          <p>${ps.recommendation}</p>
        </div>
      `;
      analysisPriorityList.appendChild(card);
    });

    // Strong Skills List
    renderMiniList(analysisStrongList, currentAnalysis.strong_skills, "text-strong");

    // Developing Skills List
    renderMiniList(analysisDevelopingList, currentAnalysis.developing_skills, "text-developing");

    // Weak Skills List
    renderMiniList(analysisWeakList, currentAnalysis.weak_skills, "text-weak");
  }

  function renderMiniList(container, items, textClass) {
    container.innerHTML = "";
    if (!items || items.length === 0) {
      container.innerHTML = `<span style="font-size: 0.85rem; color: var(--text-dim);">None</span>`;
      return;
    }

    items.forEach((item) => {
      const div = document.createElement("div");
      div.className = "skill-preview-row";
      div.innerHTML = `
        <span>${item.name} ${item.is_demonstrated ? '✓' : ''}</span>
        <span class="${textClass} font-bold">${item.proficiency}%</span>
      `;
      container.appendChild(div);
    });
  }
});
