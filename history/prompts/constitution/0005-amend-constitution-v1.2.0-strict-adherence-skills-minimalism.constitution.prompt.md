---
id: 0005
title: Amend Constitution v1.2.0 - Strict Adherence, Skills, Minimalism
stage: constitution
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: constitution-v1.1.0-pedagogical-structure
user: Alishba
command: /sp.constitution
labels: ["constitution", "governance", "beginner-focus", "skills-integration", "anti-hallucination"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Manual validation: No unresolved placeholder tokens
  - Manual validation: Version increment follows semantic versioning
  - Manual validation: All new rules include rationale
---

## Prompt

```text
update my constitution.md adding my new instructions and requirements i need to specify that my agent will not write or add features by itself which i haven't mentioned in my prompt , it has to strictly stick to my given instruction and genearte all files according to that

I am a beginner and i am not adding images video in my book at this point so remove any if instruction related to image are there.

Mention to invoke related skills present in skill.md while writing book.

Mention to stay smart and minimalistic avoiding hallucunaions and achieving goal seamlessly.
```

## Response snapshot

Constitution updated from version 1.1.0 to 1.2.0 with MINOR version bump.

**Changes implemented:**

1. **Rule 14: Strict Adherence to User Instructions** - Agent MUST generate ONLY files/features explicitly mentioned in prompts. No unsolicited improvements, refactorings, or additional features. Scope control formalized as constitutional requirement.

2. **Rule 15: Skills Invocation for Book Content** - Mandatory invocation of professional-author skill (`.claude/skills/professional-author/SKILL.md`) when authoring any textbook content. Never bypass for "quick edits."

3. **Rule 16: Smart Minimalism and Anti-Hallucination** - NEVER invent APIs, packages, configurations, or technical facts. Verify ALL claims against official 2025 docs. Surface uncertainty explicitly. Prefer simple patterns over clever abstractions.

4. **Rule 17: Post-Implementation Commit Offering** - Formalized commit workflow: offer (don't auto-commit), wait for approval, follow Rule 9 message format. Makes git operations transparent and educational.

5. **Modified Rule 4** - Removed image format requirements (WebP/300KB) to align with beginner text-only approach.

6. **Removed Documentation Standards section** - "Image and Media Standards" entirely removed (lines 104-109 in previous version).

7. **Updated Compliance Verification** - Changed from 12 rules to 17 rules monitoring.

**Sync Impact Report** (prepended to constitution.md as HTML comment):
- Templates flagged for updates: spec, plan, tasks templates need review for image/media removal and skills invocation guidance
- Follow-up TODOs: Review existing specs, align professional-author skill, create pre-commit hook for Rule 14 validation

**Version metadata updated:**
- Version: 1.2.0 (MINOR bump - new rules added)
- Ratified: 2025-12-04 (unchanged)
- Last Amended: 2025-12-05 (today)

## Outcome

- ✅ Impact: Constitution now explicitly guarantees beginner-predictable scope control, eliminates hallucination risk through mandatory verification, integrates skills framework for consistency, and removes beginner-inappropriate image requirements
- 🧪 Tests: Manual validation passed - no unresolved tokens, version coherent, all rules have rationale, sync report complete
- 📁 Files: Modified `.specify/memory/constitution.md` (version 1.1.0 → 1.2.0)
- 🔁 Next prompts: User should review dependent templates if needed; suggest commit with message `[Rule 11] docs: amend constitution to v1.2.0 - add Rules 14-17 (strict adherence, skills, minimalism, commit workflow)`
- 🧠 Reflection: Four new rules formalize informal best practices into enforceable governance. Beginner focus (Rule 14, image removal) reduces confusion. Skills integration (Rule 15) ensures consistency. Anti-hallucination (Rule 16) prevents robotics disasters. Commit workflow (Rule 17) makes git educational.

## Evaluation notes (flywheel)

- Failure modes observed: None - template requirements clear, user input unambiguous
- Graders run and results (PASS/FAIL): PASS - all validation checks passed (no placeholders, version increment correct, rationale complete, sync report generated)
- Prompt variant (if applicable): N/A - standard constitution amendment workflow
- Next experiment (smallest change to try): Monitor Rule 14 adherence in practice - does it successfully prevent scope creep? Consider adding automated pre-commit validation for unsolicited files.
