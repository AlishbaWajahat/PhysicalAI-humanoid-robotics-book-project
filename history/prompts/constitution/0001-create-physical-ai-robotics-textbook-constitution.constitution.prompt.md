---
id: 0001
title: Create Physical AI Robotics Textbook Constitution
stage: constitution
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Alishba
command: /sp.constitution
labels: ["constitution", "project-setup", "governance", "physical-ai", "robotics"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Manual validation: 12 rules present
  - Manual validation: No placeholders remaining
  - Manual validation: Version 1.0.0 set correctly
---

## Prompt

```text
generate

You are now creating the supreme, unbreakable constitution.md for the Panaversity flagship textbook:

Title: Physical AI & Humanoid Robotics – The Official AI-Native Textbook
Tech stack: Docusaurus + MDX + Spec-Kit Plus + Claude Code + GitHub Pages
Development environment: WSL Ubuntu 22.04 + RTX GPU
Authoring methodology: 100 % spec-driven via /sp.specify commands only

This constitution must function exactly like a team rulebook before building a massive LEGO cathedral: short, crystal-clear, absolute laws that both human and every Claude Code instance MUST obey for the entire project lifetime. No exceptions, no workarounds.

Model it directly on the highly successful AI-Native Software Development Book Constitution (v6+) that you already know, but perfectly tailored to Physical AI & Humanoid Robotics education.

Core requirements for the constitution you will output:

1. Short, numbered rules (max 12 rules) – think "10 Commandments" style, not long essays
2. Every rule activates reasoning mode, never prediction mode
3. Zero mention of the hackathon, deadlines, or bonus points
4. Heavy emphasis on these unbreakable laws:
   - 100 % spec-driven only → nothing is created without an explicit /sp.specify
   - Never hallucinate any technical fact about ROS 2, Gazebo, NVIDIA Isaac Sim/ROS/Lab, URDF, Jetson, Unitree, RealSense, etc. → MUST fetch and quote the latest official documentation in real time every single time
   - All installation commands, package versions, launch files, hardware specs MUST come from the official source dated 2025 or newer
   - Reproducibility on clean Ubuntu 22.04 + RTX 4070 Ti (or documented cloud equivalent) is sacred
   - Consistency police: Black + Ruff + mypy, kebab-case filenames, IEEE citations [1], images WebP <300 KB, etc.
   - Zero tolerance for outdated versions, untested code, placeholder text, or external CDNs except allowed free tiers
   - Every commit message MUST start with the exact constitution rule number it satisfies
   - Immediate stop-and-ask if anything is ambiguous → reply "Stopped – need new /sp.specify for …"
   - /status command instantly returns full compliance report against the numbered rules

5. Include the exact activation phrase at the end so I can lock it in instantly:
   Reply only with the full constitution.md content wrapped in ```markdown
   and finish with:
   "Constitution accepted. X rules locked in. Ready for the first /sp.specify"

6. Tone: Authoritative, professional, Panaversity-grade, no fluff, no explanations outside the rules themselves

Generate the constitution.md now.
```

## Response snapshot

Created comprehensive 12-rule constitution for Physical AI & Humanoid Robotics textbook with unbreakable principles:

**Core Rules Established:**
1. Specification-Driven Development Only - Nothing without `/sp.specify`
2. Real-Time Documentation Verification - Never hallucinate technical facts
3. Reproducibility on Reference Environment (Ubuntu 22.04 + RTX 4070 Ti)
4. Code Quality Enforcement (Black, Ruff, mypy, kebab-case, IEEE citations, WebP <300KB)
5. Version Precision Absolute - Exact versions always
6. Safety and Hardware Protection First
7. Test-Driven Content Development
8. External Dependency Restrictions (free-tier only)
9. Commit Message Compliance (start with rule number)
10. Docusaurus + MDX Native Content Only
11. AI-Native Authoring Workflow (PHRs + ADRs)
12. Immediate Stop on Ambiguity

**Additional Sections:**
- Documentation Standards (citation format, code blocks, images, simulation assets)
- Governance (constitutional authority, amendment process, compliance verification, versioning policy, enforcement mechanisms)

**File Created:**
- `.specify/memory/constitution.md` (v1.0.0, ratified 2025-12-04)

## Outcome

- ✅ Impact: Established constitutional foundation for entire Physical AI & Humanoid Robotics textbook project with 12 unbreakable rules governing spec-driven development, documentation verification, reproducibility, safety, and quality standards
- 🧪 Tests: Manual validation passed (12 rules present, no placeholders, version 1.0.0 correct)
- 📁 Files: Created `.specify/memory/constitution.md` (141 lines)
- 🔁 Next prompts: First `/sp.specify` for initial textbook feature/chapter; template synchronization for plan/spec/tasks templates per Sync Impact Report
- 🧠 Reflection: Constitution successfully balances rigor (real-time doc verification, version precision) with practicality (free-tier dependencies, reproducible environment). Rule 2 and Rule 12 work synergistically to prevent hallucination. Rule 6 (safety) is critical for physical robotics content.

## Evaluation notes (flywheel)

- Failure modes observed: None during generation. Potential future issues: template synchronization lag, `/status` command not yet implemented, commit hook enforcement not yet configured
- Graders run and results (PASS/FAIL): N/A (constitution baseline)
- Prompt variant (if applicable): None (initial generation)
- Next experiment (smallest change to try): Implement `/status` slash command to return compliance report; add pre-commit hook for Rule 9 (commit message format validation)
