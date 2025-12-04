<!--
Sync Impact Report:
Version change: 1.0.0 → 1.1.0 (MINOR - Added Rule 13: Pedagogical Structure)
Modified principles: None (existing rules unchanged)
Added sections: Rule 13: Pedagogical Structure Mandatory
Removed sections: None
Reason for amendment: Critical gap identified - textbook requires explicit pedagogical scaffolding standards (learning objectives, worked examples, progressive difficulty) that differ from technical documentation
Templates requiring updates:
  ✅ constitution.md (this file)
  ⚠ Spec template - MUST now include learning objectives and prerequisite sections for chapter specs
  ⚠ Plan template - MUST now include pedagogical progression planning
  ⚠ Tasks template - MUST now include tasks for creating worked examples, exercises, and chapter summaries
Follow-up TODOs:
  - Phase 2: Add Rule 14 (Interactive Learning Elements) after first chapter tested
  - Phase 3: Add Rule 15 (Accessibility WCAG 2.1 AA) during QA phase
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### Rule 1: Specification-Driven Development Only
NOTHING is authored, installed, or configured without an explicit `/sp.specify` command. No exceptions. Every chapter, code example, simulation setup, hardware instruction, or configuration file MUST originate from an approved feature specification. If ambiguity exists, STOP immediately and reply: "Stopped – need new /sp.specify for [specific requirement]."

**Rationale**: Prevents scope creep, ensures traceability, and maintains architectural coherence across a complex multi-domain textbook spanning robotics, AI, physics simulation, and hardware integration.

### Rule 2: Real-Time Documentation Verification Mandatory
NEVER hallucinate technical facts. Every installation command, API reference, package version, URDF structure, ROS 2 node configuration, Gazebo plugin, NVIDIA Isaac Sim/ROS/Lab feature, Jetson hardware spec, Unitree robot parameter, or RealSense sensor detail MUST be fetched from official documentation dated 2025 or newer and explicitly quoted with source URL.

**Rationale**: Physical AI/robotics tools evolve rapidly. Outdated or incorrect technical guidance causes installation failures, simulation crashes, and hardware damage. Real-time verification ensures students get working, current instructions.

### Rule 3: Reproducibility on Reference Environment Sacred
Every code example, installation procedure, simulation script, and hardware setup MUST be reproducible on a clean Ubuntu 22.04 LTS system with NVIDIA RTX 4070 Ti GPU (or documented cloud equivalent with equivalent CUDA compute capability). Document all system requirements, dependencies, and environmental variables explicitly.

**Rationale**: Students need a reliable reference environment. Reproducibility failures undermine trust and learning outcomes in a hardware-software co-design curriculum.

### Rule 4: Code Quality Enforcement Non-Negotiable
All Python code MUST pass Black (formatting), Ruff (linting), and mypy (type checking) with zero errors before commit. All filenames MUST use kebab-case. All citations MUST follow IEEE format [1]. All images MUST be WebP format under 300 KB. No placeholder text, no TODO comments in published content, no commented-out code.

**Rationale**: Professional-grade textbooks demand professional-grade code standards. Inconsistency degrades readability and student comprehension.

### Rule 5: Version Precision Absolute
All package versions, ROS 2 distributions, Gazebo releases, NVIDIA driver versions, CUDA toolkit versions, and hardware firmware versions MUST be explicitly specified with exact version numbers (e.g., `ros-humble-desktop=0.10.0-1`, `gazebo-11.12.0`, `CUDA 12.3`). Never use "latest," "current," or unversioned references.

**Rationale**: Version drift causes incompatibility cascades in robotics stacks. Precision enables long-term maintainability and debugging.

### Rule 6: Safety and Hardware Protection First
All hardware interaction chapters MUST include explicit safety warnings, electrical safety checklists, ESD protection protocols, emergency stop procedures, and failure mode documentation. All simulation chapters MUST include resource limits (CPU, GPU, memory) and graceful degradation strategies. Never assume prior hardware experience.

**Rationale**: Physical AI involves real robots, high-voltage power supplies, moving actuators, and expensive sensors. Student safety and equipment protection are paramount.

### Rule 7: Test-Driven Content Development
Every code example MUST include: (1) Expected output, (2) Common failure modes, (3) Verification command to confirm success, (4) Troubleshooting steps for top 3 failure scenarios. Simulation chapters MUST include visual validation criteria (screenshots, video references with timestamps). Hardware chapters MUST include sensor output validation ranges.

**Rationale**: Robotics debugging is notoriously difficult. Pre-validated test criteria reduce student frustration and support scalability.

### Rule 8: External Dependency Restrictions
ONLY use free-tier or open-source external services explicitly approved: GitHub Pages (hosting), GitHub Actions (CI/CD), Docker Hub free tier (container registry), NVIDIA NGC free tier (pre-built containers). Absolutely NO paid APIs, premium CDNs, or services requiring credit cards. All dependencies MUST be declaratively specified in version-controlled configuration files.

**Rationale**: Textbook accessibility requires zero financial barriers for students. Dependency clarity enables offline/airgapped environments common in academic labs.

### Rule 9: Commit Message Compliance Mandatory
Every commit message MUST start with the exact constitution rule number it satisfies (e.g., `[Rule 2] Add verified ROS 2 Humble installation steps from official docs 2025-11`). Commits spanning multiple rules MUST list all (e.g., `[Rule 2,5] Verify Isaac Sim 4.0.0 Python API with version pin`).

**Rationale**: Enables instant compliance auditing via git log, reinforces rule awareness, and facilitates automated constitutional adherence checks.

### Rule 10: Docusaurus + MDX Native Content Only
All educational content MUST be authored in MDX (Markdown + JSX) compatible with Docusaurus 3.x. NEVER use proprietary formats, binary word processor files, or external rendering dependencies. All interactive components MUST be React components in the `/src/components` directory with TypeScript definitions and documented props.

**Rationale**: Ensures version control effectiveness, enables component reuse, and maintains long-term editorial control without vendor lock-in.

### Rule 11: AI-Native Authoring Workflow
This textbook is authored EXCLUSIVELY via Claude Code + Spec-Kit Plus workflows. All content generation MUST preserve complete reasoning traces via Prompt History Records (PHRs) in `history/prompts/`. Architectural decisions MUST be captured in ADRs in `history/adr/` when passing the three-part significance test (impact + alternatives + scope).

**Rationale**: Transparency in AI-assisted authoring establishes trust, enables quality auditing, and creates a reusable methodology for future AI-native educational content.

### Rule 12: Immediate Stop on Ambiguity
If ANY requirement is ambiguous, incomplete, or conflicts with existing specifications, STOP all work immediately and request clarification. NEVER assume, improvise, or "fill in the gaps" based on general knowledge. Ask targeted questions that resolve the specific ambiguity.

**Rationale**: In multi-domain robotics projects, assumptions compound exponentially. Explicit clarification prevents costly rework and maintains specification integrity.

### Rule 13: Pedagogical Structure Mandatory
Every chapter MUST include: (1) Learning objectives using measurable verbs (understand, implement, analyze, debug, evaluate), (2) Explicit prerequisites with links to prior chapters or external resources, (3) Worked examples with step-by-step explanations BEFORE practice exercises, (4) Practice problems with solution hints (not full solutions in main text), (5) Chapter summary with 3-5 key takeaways. Difficulty MUST progress within chapters: concept introduction → demonstration → guided practice → independent challenge.

**Rationale**: Textbooks require pedagogical scaffolding that differs fundamentally from documentation. Progressive difficulty builds confidence and prevents cognitive overload. Explicit learning objectives enable students to self-assess mastery and instructors to design assessments aligned with content.

## Documentation Standards

### Citation Format
All external references MUST use IEEE citation style: [1], [2], etc., with full bibliography at chapter end including:
- Author(s)
- Title
- Publication/Organization
- URL (for online resources)
- Access date (YYYY-MM-DD)

### Code Block Requirements
All code blocks MUST include:
- Language identifier for syntax highlighting (```python, ```bash, ```xml, etc.)
- File path comment on first line if representing a file (e.g., `# File: src/robot_controller.py`)
- Inline comments explaining non-obvious logic
- Expected output as comment block after code

### Image and Media Standards
- WebP format exclusively
- Max 300 KB file size (use lossy compression if needed)
- Descriptive alt text for accessibility
- Caption with figure number (e.g., "Figure 3.2: ROS 2 node graph for navigation stack")
- Source attribution if not original

### Simulation Asset Management
All 3D models, URDF files, mesh files, and simulation worlds MUST:
- Be stored in `/static/simulation-assets/` organized by chapter
- Include license information (preferably CC-BY-4.0 or Apache-2.0)
- Document coordinate frame conventions (ROS standard: X forward, Y left, Z up)
- Specify units explicitly (meters, kilograms, seconds)

## Governance

### Constitutional Authority
This constitution supersedes all other practices, preferences, or conventions. No work proceeds that violates these rules. In case of conflict between rule interpretations, work stops until clarification is obtained.

### Amendment Process
Constitution amendments require:
1. Documented justification referencing specific project needs
2. Approval via explicit user consent
3. Version increment following semantic versioning (MAJOR.MINOR.PATCH)
4. Propagation to all dependent templates (`plan-template.md`, `spec-template.md`, `tasks-template.md`)
5. Announcement in project changelog with migration guidance

### Compliance Verification
The `/status` slash command MUST return:
- Compliance status for each of the 12 rules
- Last commit verification (rule number present in message)
- Last documentation verification timestamp (Rule 2)
- Template synchronization status
- Outstanding constitutional violations (if any)

### Versioning Policy
- MAJOR: Backward-incompatible rule changes or removals
- MINOR: New rules added or existing rules materially expanded
- PATCH: Clarifications, examples, non-semantic wording improvements

### Enforcement Mechanisms
- Pre-commit hooks validate: code formatting (Rule 4), version specifications (Rule 5), commit message format (Rule 9)
- CI/CD pipeline gates: reproducibility tests (Rule 3), external dependency audit (Rule 8), documentation verification timestamps (Rule 2)
- Human review required for: safety content (Rule 6), architectural decisions (Rule 11), constitutional amendments (this section)

**Version**: 1.1.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-04
