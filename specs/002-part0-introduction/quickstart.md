# Quickstart: Part 0 Introduction Structure Implementation

**Date**: 2025-12-05
**Feature**: 002-part0-introduction
**Estimated Implementation Time**: 15-20 minutes

## Prerequisites

- Docusaurus 3.9.2 installed (verify with `npm list @docusaurus/core`)
- Node.js >=20.0 (verify with `node --version`)
- On feature branch `002-part0-introduction`
- Repository root: `D:/Alishba/Documents/projects/spec-driven-dev/cloned/PhysicalAI-humanoid-robotics-book-project`

## Implementation Steps

### Step 1: Create Directory Structure

```bash
# From repository root
mkdir -p docs/part0-introduction
```

**Verification**: `ls docs/part0-introduction` should succeed (directory exists)

---

### Step 2: Create Introduction Document

**File**: `docs/part0-introduction/part0-introduction.mdx`

**Content**:
```markdown
---
id: part0-introduction
title: Introduction to physical AI and humanoid robotics
sidebar_label: Introduction to physical AI and humanoid robotics
description: Foundational introduction to the field of physical AI and humanoid robotics, covering core concepts and the spec-driven development workflow.
---

# Introduction to physical AI and humanoid robotics
```

**Notes**:
- YAML frontmatter must be enclosed in `---` delimiters
- Optional h1 heading provided for authoring convenience (not required per spec)
- Em dash (—) not present in this title

**Verification**: File exists and is valid UTF-8

---

### Step 3: Create Chapter 1 Document

**File**: `docs/part0-introduction/chapter-1-why-physical-ai-is-the-next-frontier.mdx`

**Content**:
```markdown
---
id: chapter-1-why-physical-ai-is-the-next-frontier
title: Chapter 1 — Why Physical AI Is the Next Frontier
sidebar_label: Chapter 1 — Why Physical AI Is the Next Frontier
description: Explores why physical AI represents the next major frontier in artificial intelligence and robotics.
---

# Chapter 1 — Why Physical AI Is the Next Frontier
```

**Notes**:
- Filename uses hyphens (kebab-case per Rule 4)
- Title and sidebar_label use em dash (—) character per spec
- Ensure UTF-8 encoding when creating file

**Verification**: File exists, em dash displays correctly in editor

---

### Step 4: Create Chapter 2 Document

**File**: `docs/part0-introduction/chapter-2-the-new-workflow-spec-driven-physical-ai.mdx`

**Content**:
```markdown
---
id: chapter-2-the-new-workflow-spec-driven-physical-ai
title: Chapter 2 — The New Workflow: Spec-Driven Physical AI
sidebar_label: Chapter 2 — The New Workflow: Spec-Driven Physical AI
description: Introduces the spec-driven development workflow for physical AI projects, combining specification-first design with iterative implementation.
---

# Chapter 2 — The New Workflow: Spec-Driven Physical AI
```

**Notes**:
- Filename uses hyphens (kebab-case per Rule 4)
- Title includes colon and em dash per spec
- Description explains the workflow concept

**Verification**: File exists, special characters display correctly

---

### Step 5: Update Sidebar Configuration

**File**: `sidebars.js` (repository root)

**Action**: Replace the existing `tutorialSidebar` array with:

```javascript
tutorialSidebar: [
  {
    type: 'category',
    label: 'Introduction to physical AI and humanoid robotics',
    items: [
      'part0-introduction/part0-introduction',
      'part0-introduction/chapter-1-why-physical-ai-is-the-next-frontier',
      'part0-introduction/chapter-2-the-new-workflow-spec-driven-physical-ai'
    ]
  }
]
```

**Current content** (before modification):
```javascript
tutorialSidebar: [
  'hello',
  {
    type: 'category',
    label: 'TutoriaL',
    items: ['tutorial-basics/create-a-document'],
  },
],
```

**Action**: **REPLACE** with new structure (remove 'hello' and 'TutoriaL' category)

**Notes**:
- Use document IDs (relative to `docs/` directory)
- Do NOT include `.mdx` extension in IDs
- Maintain JavaScript syntax (commas, quotes, brackets)
- Label exactly matches introduction title

**Verification**: File is valid JavaScript (no syntax errors)

---

### Step 6: Validate Build

```bash
# From repository root
npm run build
```

**Expected Output**:
- Build completes without errors
- No warnings about missing docs or broken links
- Output includes "Success!" message

**If build fails**:
1. Check for YAML syntax errors in frontmatter (missing quotes, colons, dashes)
2. Verify document IDs in sidebar match frontmatter IDs
3. Ensure all file paths are correct
4. Check for UTF-8 encoding issues

---

### Step 7: Verify Development Server

```bash
# From repository root
npm start
```

**Expected Behavior**:
1. Dev server starts on http://localhost:3000
2. Sidebar displays "Introduction to physical AI and humanoid robotics" as expandable category
3. Category expands to show 3 items:
   - Introduction to physical AI and humanoid robotics
   - Chapter 1 — Why Physical AI Is the Next Frontier
   - Chapter 2 — The New Workflow: Spec-Driven Physical AI
4. Clicking each item loads page with correct title
5. Em dash (—) renders correctly in browser

**Verification Checklist**:
- [ ] Sidebar category label matches spec exactly
- [ ] All 3 items appear in correct order
- [ ] Em dash character displays correctly (not as HTML entity or garbled)
- [ ] Each page loads without console errors
- [ ] Page titles match frontmatter titles
- [ ] No placeholder or Lorem ipsum text visible

---

### Step 8: Final File Structure Verification

```bash
# From repository root
tree docs/part0-introduction
```

**Expected structure**:
```
docs/part0-introduction/
├── part0-introduction.mdx
├── chapter-1-why-physical-ai-is-the-next-frontier.mdx
└── chapter-2-the-new-workflow-spec-driven-physical-ai.mdx
```

**File count**: Exactly 3 files, no subdirectories

**Filename validation**:
- All lowercase
- All use hyphens (no underscores or spaces)
- All end in `.mdx` extension
- No special characters except hyphens

---

## Acceptance Criteria Validation

Map implementation to spec success criteria:

### SC-001: `npm start` builds successfully ✅
- Verified in Step 7

### SC-002: Sidebar displays category with 2 child chapters ✅
- Verified in Step 7 (actually 3 items: intro + 2 chapters)

### SC-003: All 3 documents accessible via navigation ✅
- Verified in Step 7 (click-through test)

### SC-004: Kebab-case filenames in correct directory ✅
- Verified in Step 8

### SC-005: Frontmatter validation ✅
- Each file has id, title, sidebar_label, description
- Verified in Steps 2-4

### SC-006: `npm run build` completes without warnings ✅
- Verified in Step 6

### SC-007: Em dash renders correctly ✅
- Verified in Step 7 (visual browser check)

---

## Troubleshooting Guide

### Issue: Build fails with "Cannot find module"

**Cause**: Document ID in sidebar doesn't match file path

**Fix**:
1. Verify IDs in `sidebars.js` match format: `part0-introduction/filename-without-extension`
2. Ensure files exist at `docs/part0-introduction/`
3. Check spelling carefully (hyphens vs underscores)

### Issue: Em dash displays as � or &#8212;

**Cause**: File encoding is not UTF-8

**Fix**:
1. Re-save files with UTF-8 encoding in your editor
2. On Windows: Use UTF-8 without BOM
3. Verify with: `file -i filename.mdx` (should show charset=utf-8)

### Issue: Sidebar shows "Tutorial" instead of "Introduction"

**Cause**: Old sidebar configuration still active

**Fix**:
1. Verify you replaced (not appended) content in `sidebars.js`
2. Clear Docusaurus cache: `npm run clear`
3. Restart dev server: Ctrl+C then `npm start`

### Issue: Page shows frontmatter as text

**Cause**: Missing `---` delimiters or invalid YAML

**Fix**:
1. Ensure frontmatter starts with `---` on line 1
2. Ensure frontmatter ends with `---` on its own line
3. Check for proper indentation (YAML is whitespace-sensitive)
4. Validate YAML syntax online if needed

### Issue: Pages load but titles are wrong

**Cause**: Mismatch between frontmatter `title` and `sidebar_label`

**Fix**:
1. Ensure `title` and `sidebar_label` are identical in each file
2. Verify exact character matching (em dash, colons, capitalization)
3. Check for trailing spaces in YAML values

---

## Post-Implementation Checklist

- [ ] All 3 MDX files created in `docs/part0-introduction/`
- [ ] All files use kebab-case filenames
- [ ] All frontmatter fields present and correct
- [ ] `sidebars.js` updated with new category
- [ ] `npm run build` succeeds
- [ ] `npm start` works and shows correct structure
- [ ] Em dash character renders correctly
- [ ] No placeholder or TODO content in files
- [ ] Git status shows 4 new/modified files (3 MDX + 1 sidebars.js)

---

## Next Steps

After implementation complete:

1. **Create tasks**: Run `/sp.tasks` to generate implementation tasks
2. **Implement tasks**: Execute tasks in order (file creation, sidebar update, validation)
3. **Test**: Verify all acceptance criteria pass
4. **Commit**: Create commit per Rule 9 format

**Estimated total time**: 15-20 minutes for experienced developers, 25-30 minutes for beginners

## References

- Research findings: [research.md](./research.md)
- Data model: [data-model.md](./data-model.md)
- Feature spec: [spec.md](./spec.md)
- Docusaurus docs: https://docusaurus.io/docs/3.9.2
