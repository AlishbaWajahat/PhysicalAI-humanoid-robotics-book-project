# Implementation Plan: Minimal Docusaurus v3 Setup

**Branch**: `001-docusaurus-setup` | **Date**: 2025-12-04 | **Spec**: [spec.md](./spec.md)

## Summary

Initialize minimal Docusaurus v3.9.2 static site with JavaScript, classic preset, and SASS support. Site runs on localhost:3000 with title "Physical AI & Humanoid Robotics". No math plugins, no TypeScript, no deployment - just a clean dev environment ready for textbook authoring.

## Technical Context

**Language/Version**: JavaScript (ES2022), Node.js v20.x LTS, React 18.x (Docusaurus dependency)
**Primary Dependencies**:
- @docusaurus/core 3.9.2
- @docusaurus/preset-classic 3.9.2
- docusaurus-plugin-sass (latest)
- sass (peer dependency)

**Storage**: Static files (no database)
**Testing**: Manual browser verification
**Target Platform**: WSL2 Ubuntu 22.04, localhost development
**Project Type**: Static site generator (web documentation)
**Performance Goals**:
- Dev server startup: <5 seconds
- Hot reload: <2 seconds
- Page load: <1 second

**Constraints**:
- JavaScript only (no TypeScript)
- Classic preset only
- Minimal dependencies
- Must work offline after npm install

**Scale/Scope**: Single intro page, expandable to 50-100 chapters

## Constitution Check

*GATE: Must pass before Phase 0*

### Rule 1 (Specification-Driven Development): ✅ PASS
- Originates from explicit SETUP-001 spec

### Rule 2 (Documentation Verification): ✅ PASS
- Docusaurus version verified from https://docusaurus.io (December 2025)
- Will verify exact version during Phase 0

### Rule 3 (Reproducibility): ✅ PASS
- Target: Ubuntu 22.04 + Node v20.x
- All dependencies locked in package-lock.json

### Rule 4 (Code Quality): ✅ PASS
- JavaScript follows standard formatting
- Kebab-case filenames

### Rule 5 (Version Precision): ⚠️ PHASE 0
- NEEDS RESEARCH: Exact Docusaurus version (3.9.x latest)
- NEEDS RESEARCH: Compatible docusaurus-plugin-sass version

### Rule 6 (Safety): ✅ N/A
- No hardware, no safety concerns

### Rule 7 (Test-Driven): ✅ PASS
- Spec includes verification: `npm run start` succeeds
- Edge cases documented

### Rule 8 (Dependencies): ✅ PASS
- All free/open-source (npm packages)
- No paid services

### Rule 9 (Commit Messages): ✅ PASS
- Required format: "Rule 1 + SETUP-001: Minimal Docusaurus v3 ready"

### Rule 10 (Docusaurus + MDX): ✅ PASS
- This IS the Docusaurus setup

### Rule 11 (AI-Native Workflow): ✅ PASS
- Using Claude Code + Spec-Kit Plus
- PHR will be created

### Rule 12 (Stop on Ambiguity): ✅ PASS
- All requirements clear

### Rule 13 (Pedagogical Structure): ✅ N/A
- Infrastructure setup, not educational content

**GATE STATUS**: ✅ PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```
specs/001-docusaurus-setup/
├── spec.md              # ✅ Complete
├── plan.md              # ⬅ This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/           # Phase 1 (empty, .gitkeep only)
└── tasks.md             # Phase 2 (/sp.tasks command)
```

### Source Code (repository root)

```
# Docusaurus standard structure

docs/
├── intro.md             # Welcome page
└── _category_.json      # Sidebar config

static/
└── img/
    ├── logo.svg
    └── favicon.ico

src/
├── components/          # Custom React components
├── css/
│   └── custom.css       # Global styles
└── pages/
    └── index.js         # Landing page

# Root config files
docusaurus.config.js     # Main configuration
sidebars.js              # Sidebar structure
package.json             # Dependencies
package-lock.json        # Locked versions
babel.config.js          # Babel config (auto-generated)
.gitignore               # Docusaurus defaults
```

**Structure Decision**: Standard Docusaurus layout - no customization needed for minimal setup.

## Phase 0: Research

### Research Tasks

**RT-001: Verify Latest Docusaurus Version**
- **Question**: What is the exact latest stable Docusaurus v3 version as of December 2025?
- **Method**: Fetch from https://docusaurus.io
- **Decision Criteria**: Use latest stable 3.x release

**RT-002: SASS Plugin Compatibility**
- **Question**: What version of docusaurus-plugin-sass is compatible with latest Docusaurus v3?
- **Method**: Check npm registry, plugin documentation
- **Decision Criteria**: Latest version with Docusaurus v3 support

## Phase 1: Design

### Step-by-Step Setup (for quickstart.md)

1. Initialize Docusaurus with classic preset
2. Install SASS plugin + dependencies
3. Configure docusaurus.config.js (title, tagline)
4. Verify dev server starts
5. Git commit and push

### Configuration Data Model (for data-model.md)

Key configuration object in `docusaurus.config.js`:
- `title`: "Physical AI & Humanoid Robotics"
- `tagline`: "The Official Panaversity AI-Native Textbook"
- `url`: "http://localhost:3000" (temporary)
- `baseUrl`: "/"
- Plugins: [@docusaurus/preset-classic, docusaurus-plugin-sass]

### Contracts

N/A - Static site has no API contracts. Will create empty `contracts/` directory with `.gitkeep`.

## Execution Plan (Step-by-Step)

Following spec requirement for incremental commands:

### Step 1: Initialize Docusaurus
```bash
npx create-docusaurus@latest my-website classic --javascript
```

### Step 2: Move files to root
```bash
cd my-website && mv * .. && mv .gitignore .. && mv .* .. 2>/dev/null || true; cd .. && rmdir my-website
```

### Step 3: Install SASS support
```bash
npm install --save docusaurus-plugin-sass sass
```

### Step 4: Update config
Edit `docusaurus.config.js` to add:
- title, tagline
- SASS plugin

### Step 5: Test
```bash
npm run start
```

### Step 6: Commit
```bash
git add .
git commit -m "Rule 1 + SETUP-001: Minimal Docusaurus v3 ready"
git push
```

## Success Validation

- [ ] Phase 0: research.md created with exact versions
- [ ] Phase 1: data-model.md created
- [ ] Phase 1: quickstart.md created with step-by-step commands
- [ ] Phase 1: contracts/ directory exists
- [ ] Ready for /sp.tasks

## Notes

- Minimal setup - no math, no deployment, no extras
- Incremental execution per spec requirements
- After planning: proceed to step-by-step implementation
