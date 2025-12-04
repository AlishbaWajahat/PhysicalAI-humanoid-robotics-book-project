# Quickstart Guide: Minimal Docusaurus v3 Setup

**Feature**: 001-docusaurus-setup
**Phase**: Phase 1
**Date**: 2025-12-04

## Prerequisites

- Node.js v20.x LTS installed
- Git configured with remote origin
- Currently in project root directory
- Network connectivity for npm

## Step-by-Step Execution

### Step 1: Initialize Docusaurus

Run this command to create a new Docusaurus site with the classic preset and JavaScript (no TypeScript):

```bash
npx create-docusaurus@latest my-website classic --javascript
```

**What it does**:
- Downloads and runs Docusaurus scaffolding tool
- Creates `my-website` directory with complete Docusaurus structure
- Uses classic preset (standard theme and plugins)
- Configures for JavaScript only (no TypeScript)

**Expected output**:
```
Creating new Docusaurus project...
✔ Installation complete!
```

**Wait for** "done" from user before proceeding.

---

### Step 2: Move Files to Root

Move all Docusaurus files from `my-website/` to project root:

```bash
cd my-website && mv * .. && mv .gitignore .. && cd .. && rmdir my-website
```

**What it does**:
- Enters my-website directory
- Moves all visible files to parent (project root)
- Moves .gitignore separately
- Returns to project root
- Removes empty my-website directory

**Expected result**:
- docusaurus.config.js now in root
- docs/ directory in root
- src/ directory in root
- static/ directory in root

**Wait for** "done" from user before proceeding.

---

### Step 3: Install SASS Support

Install the SASS plugin and its peer dependency:

```bash
npm install --save docusaurus-plugin-sass sass
```

**What it does**:
- Installs docusaurus-plugin-sass v0.2.6
- Installs sass (Dart Sass)
- Adds both to package.json dependencies
- Updates package-lock.json

**Expected output**:
```
added 2 packages
```

**Wait for** "done" from user before proceeding.

---

### Step 4: Update Configuration

Edit `docusaurus.config.js` to customize title, tagline, and add SASS plugin.

**Find these lines**:
```javascript
title: 'My Site',
tagline: 'Dinosaurs are cool',
```

**Replace with**:
```javascript
title: 'Physical AI & Humanoid Robotics',
tagline: 'The Official Panaversity AI-Native Textbook',
```

**Find the plugins array** (add if it doesn't exist):
```javascript
plugins: [],
```

**Replace with**:
```javascript
plugins: [
  'docusaurus-plugin-sass',
],
```

**Manual edit required** - confirm when complete.

**Wait for** "done" from user before proceeding.

---

### Step 5: Test Development Server

Start the development server to verify everything works:

```bash
npm run start
```

**What it does**:
- Starts Webpack dev server
- Compiles React components
- Opens browser at http://localhost:3000
- Enables hot reload for file changes

**Expected output**:
```
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

**Verification**:
- Browser opens automatically
- See title: "Physical AI & Humanoid Robotics"
- See tagline: "The Official Panaversity AI-Native Textbook"
- Page loads in <5 seconds with zero errors

**Press Ctrl+C** to stop the dev server when verified.

**Wait for** "done" from user before proceeding.

---

### Step 6: Git Commit and Push

Commit the setup with proper message format:

```bash
git add .
git commit -m "Rule 1 + SETUP-001: Minimal Docusaurus v3 ready"
git push
```

**What it does**:
- Stages all new/modified files
- Creates commit with constitution-compliant message
- Pushes to remote origin

**Expected output**:
```
[001-docusaurus-setup xxxxx] Rule 1 + SETUP-001: Minimal Docusaurus v3 ready
 X files changed, Y insertions(+)
To [remote-url]
   xxxxx..xxxxx  001-docusaurus-setup -> 001-docusaurus-setup
```

**Final verification**:
```bash
git log -1 --oneline
```

Should show: "Rule 1 + SETUP-001: Minimal Docusaurus v3 ready"

---

## Success Criteria Checklist

- [ ] Step 1: Docusaurus initialized in my-website/
- [ ] Step 2: Files moved to project root
- [ ] Step 3: SASS plugin installed
- [ ] Step 4: Config updated with title/tagline/plugin
- [ ] Step 5: Dev server starts on localhost:3000
- [ ] Step 5: Title and tagline display correctly
- [ ] Step 5: Page loads in <5 seconds with zero errors
- [ ] Step 6: Commit created with exact message format
- [ ] Step 6: Commit pushed to remote successfully

## Troubleshooting

### Port 3000 already in use
```bash
npm run start -- --port 3001
```

### npm install fails
- Check internet connection
- Try: `npm cache clean --force`
- Then retry install

### Git push fails
- Verify remote: `git remote -v`
- Check authentication
- Ensure branch is tracking remote

## Next Steps

After completing this quickstart:
1. Run `/sp.tasks` to generate implementation tasks
2. Execute tasks to implement the setup
3. Verify all success criteria pass
