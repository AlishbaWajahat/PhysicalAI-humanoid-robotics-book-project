# Data Model: Part 0 Introduction Document Structure

**Date**: 2025-12-05
**Feature**: 002-part0-introduction

## Entity Overview

This feature manages four primary entities representing the document structure for Part 0:

1. **IntroductionDocument** - Main landing page for Part 0
2. **ChapterDocument** - Individual chapter files (×2)
3. **SidebarCategory** - Navigation structure configuration
4. **DocumentFrontmatter** - Metadata schema (shared by all documents)

## Entity Definitions

### DocumentFrontmatter (Shared Schema)

Metadata structure used by all MDX documents in this feature.

**Fields**:

| Field | Type | Required | Validation | Example |
|-------|------|----------|------------|---------|
| `id` | string | Yes | kebab-case, no special chars except hyphens | `part0-introduction` |
| `title` | string | Yes | Exact match per spec, may include em dash (—) | `Introduction to physical AI and humanoid robotics` |
| `sidebar_label` | string | Yes | Exact match per spec, may include em dash (—) | `Introduction to physical AI and humanoid robotics` |
| `description` | string | Yes | Brief summary for SEO and doc cards | `Foundational introduction to physical AI...` |

**Validation Rules**:
- `id` must be unique across all docs
- `title` and `sidebar_label` must exactly match spec requirements (FR-011)
- `description` should be 1-2 sentences, descriptive but concise
- All strings must be valid YAML (properly quoted if containing special characters)

**State**: Immutable after creation (until content authoring phase)

---

### IntroductionDocument

Main landing page acting as category introduction.

**File Properties**:

| Property | Value | Rationale |
|----------|-------|-----------|
| Path | `docs/part0-introduction/part0-introduction.mdx` | Standard Docusaurus docs structure |
| Directory | `docs/part0-introduction/` | Feature-specific subdirectory |
| Filename | `part0-introduction.mdx` | Kebab-case per Rule 4 |
| Extension | `.mdx` | MDX format per Rule 10 |

**Frontmatter Schema**:

```yaml
id: part0-introduction
title: Introduction to physical AI and humanoid robotics
sidebar_label: Introduction to physical AI and humanoid robotics
description: Foundational introduction to the field of physical AI and humanoid robotics, covering core concepts and the spec-driven development workflow.
```

**Content Structure**:
- Empty body (per FR-012: no placeholder content)
- Optional: Single h1 heading matching title for authoring convenience

**Relationships**:
- Parent in sidebar hierarchy (contains 2 child chapters)
- Referenced in `tutorialSidebar` as category item

---

### ChapterDocument

Individual chapter files (2 instances).

**File Properties (Chapter 1)**:

| Property | Value | Rationale |
|----------|-------|-----------|
| Path | `docs/part0-introduction/chapter-1-why-physical-ai-is-the-next-frontier.mdx` | Within part0 directory |
| Filename | `chapter-1-why-physical-ai-is-the-next-frontier.mdx` | Kebab-case conversion of title |
| Extension | `.mdx` | MDX format per Rule 10 |

**Frontmatter Schema (Chapter 1)**:

```yaml
id: chapter-1-why-physical-ai-is-the-next-frontier
title: Chapter 1 — Why Physical AI Is the Next Frontier
sidebar_label: Chapter 1 — Why Physical AI Is the Next Frontier
description: Explores why physical AI represents the next major frontier in artificial intelligence and robotics.
```

**File Properties (Chapter 2)**:

| Property | Value | Rationale |
|----------|-------|-----------|
| Path | `docs/part0-introduction/chapter-2-the-new-workflow-spec-driven-physical-ai.mdx` | Within part0 directory |
| Filename | `chapter-2-the-new-workflow-spec-driven-physical-ai.mdx` | Kebab-case conversion of title |
| Extension | `.mdx` | MDX format per Rule 10 |

**Frontmatter Schema (Chapter 2)**:

```yaml
id: chapter-2-the-new-workflow-spec-driven-physical-ai
title: Chapter 2 — The New Workflow: Spec-Driven Physical AI
sidebar_label: Chapter 2 — The New Workflow: Spec-Driven Physical AI
description: Introduces the spec-driven development workflow for physical AI projects, combining specification-first design with iterative implementation.
```

**Content Structure** (both chapters):
- Empty body (per FR-012: no placeholder content)
- Optional: Single h1 heading matching title for authoring convenience

**Relationships**:
- Children in sidebar hierarchy (under Introduction parent)
- Referenced in `tutorialSidebar` items array

---

### SidebarCategory

Navigation structure configuration in `sidebars.js`.

**Structure**:

```javascript
{
  type: 'category',
  label: 'Introduction to physical AI and humanoid robotics',
  items: [
    'part0-introduction/part0-introduction',
    'part0-introduction/chapter-1-why-physical-ai-is-the-next-frontier',
    'part0-introduction/chapter-2-the-new-workflow-spec-driven-physical-ai'
  ]
}
```

**Fields**:

| Field | Type | Value | Validation |
|-------|------|-------|------------|
| `type` | string | `'category'` | Must be 'category' for hierarchical grouping |
| `label` | string | `'Introduction to physical AI and humanoid robotics'` | Exact match to spec (FR-011) |
| `items` | string[] | Array of 3 document IDs | Must reference existing docs with valid IDs |

**Validation Rules**:
- `items` array must contain valid document IDs (format: `directory/filename-without-extension`)
- Document IDs must exist as actual MDX files in `docs/` directory
- Order in array determines display order in sidebar

**Relationships**:
- Parent container for 3 document references
- Part of `tutorialSidebar` configuration
- Label must match introduction document title

---

## Data Flow

```
User navigates to docs
        ↓
Docusaurus reads sidebars.js
        ↓
Renders SidebarCategory
        ↓
Lists 3 items (intro + 2 chapters)
        ↓
User clicks chapter link
        ↓
Docusaurus loads MDX file
        ↓
Renders page with frontmatter title
        ↓
Displays empty content body
```

## Constraints and Invariants

### File System Constraints
1. All files must exist at specified paths before sidebar references them
2. Directory `docs/part0-introduction/` must exist before files are created
3. Filenames must use UTF-8 encoding to support em dash in content (not filename)

### Frontmatter Constraints
1. `id` must be unique across entire docs directory
2. `title` and `sidebar_label` must exactly match spec requirements
3. All YAML must be valid and parseable by Docusaurus

### Sidebar Constraints
1. `items` array IDs must match actual document `id` fields in frontmatter
2. Category `label` must exactly match introduction title
3. Sidebar must be valid JavaScript (proper syntax, exports)

### Content Constraints
1. Body must be empty or contain only minimal heading (Rule 14: strict adherence)
2. No placeholder text, TODO comments, or Lorem ipsum (per constitution)
3. Files must be valid MDX (parseable by @mdx-js/react ^3.0.0)

## Migration Notes

**From**: Empty state (no Part 0 docs exist)
**To**: Structured empty files with complete frontmatter

**No data migration required** - this is net-new structure creation.

**Rollback strategy**: Delete `docs/part0-introduction/` directory and remove sidebar category from `sidebars.js`.

## Validation Schema

**Frontmatter validation** (applies to all 3 documents):

```typescript
interface DocumentFrontmatter {
  id: string; // matches /^[a-z0-9-]+$/
  title: string; // non-empty, matches spec exactly
  sidebar_label: string; // non-empty, matches spec exactly
  description: string; // non-empty, 1-3 sentences
}
```

**Sidebar validation**:

```typescript
interface SidebarCategory {
  type: 'category';
  label: string; // matches spec exactly
  items: string[]; // length === 3, all valid doc IDs
}
```

## Testing Strategy

### Entity Creation Tests
1. Verify all 3 MDX files exist at correct paths
2. Verify frontmatter parses as valid YAML
3. Verify all required frontmatter fields present

### Relationship Tests
1. Verify sidebar item IDs match document IDs
2. Verify sidebar category label matches introduction title
3. Verify all referenced docs exist before build

### Content Tests
1. Verify file bodies are empty (or contain only h1)
2. Verify no placeholder text present
3. Verify em dash (—) character renders correctly in browser

### Integration Tests
1. Run `npm start` - dev server starts without errors
2. Navigate to sidebar - category expands showing 3 items
3. Click each item - page loads with correct title
4. Run `npm run build` - build succeeds without warnings
