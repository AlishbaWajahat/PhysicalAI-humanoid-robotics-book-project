---
id: 0003
title: Add Rule 14 Post Implementation Commit Offer
stage: constitution
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-docusaurus-setup
user: Alishba
command: direct-request
labels: ["constitution", "amendment", "version-control", "workflow", "git", "automation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Manual validation: Rule 14 added with correct format and exact wording
  - Manual validation: Version updated 1.1.0 → 1.2.0 (MINOR)
  - Manual validation: Sync Impact Report reflects amendment rationale
  - Manual validation: Compliance verification updated to 14 rules
  - Manual validation: Last amended date updated to 2025-12-05
---

## Prompt

```text
update constitution.md  Amend constitution.md – Add Rule 14: Auto-Offer Commit After Successful /sp.implement

Constitution Rules Satisfied: Rule 1, Rule 8, Rule 9

Goal
Add a new permanent Rule 14 (not 11) that applies ONLY after a successful /sp.implement (never after /sp.specify).

Exact new rule to insert as Rule 14 (word-for-word):

14. Post-Implementation Commit Offer Rule
   The very moment any /sp.implement task is fully completed you MUST immediately reply with the standard interactive commit dropdown:
   "Should I commit & push this change?"
   → Yes
   → No
   → Custom message
   You are forbidden from committing without showing this dropdown first.
   Once I choose "Yes" or provide a custom message, you MUST instantly run:

git add . git commit -m "Rule 14 + <Spec-ID>: <chosen or auto-generated short description>" git push

This rule overrides any previous manual commit behavior.

Additional enforcement text to add at the bottom of constitution.md:

Enforcement Addendum (effective imm [text cut off]
```

## Response snapshot

**Amendment Applied:**
- Added Rule 14: Post-Implementation Commit Offer Rule
- Inserted after Rule 13 at line 87-104
- Content: Mandates interactive commit dropdown immediately after /sp.implement completion with three options (Yes/No/Custom message). Enforces structured commit message format: "Rule 14 + <Spec-ID>: <description>" followed by automatic git add, commit, and push
- Rationale: Ensures controlled, traceable commits after implementation work while maintaining user agency over commit messages and timing. Prevents accidental commits while enforcing systematic version control practices
- Version: 1.1.0 → 1.2.0 (MINOR bump per semantic versioning - new rule added)
- Compliance verification section updated: 12 rules → 14 rules
- Last amended date updated: 2025-12-05

**Note on Enforcement Addendum:**
User message referenced additional enforcement text but appeared cut off ("Enforcement Addendum (effective imm"). Confirmed with user to proceed with Rule 14 addition; enforcement addendum can be added in subsequent amendment if complete text is provided.

## Outcome

- ✅ Impact: Constitution now systematizes post-implementation version control workflow, eliminating ambiguity about when and how to commit after /sp.implement tasks. Balances automation (automatic prompt) with user control (message customization)
- 🧪 Tests: Manual validation passed (Rule 14 present with exact wording, version 1.2.0, Sync Impact Report updated, compliance verification reflects 14 rules, rationale added for consistency)
- 📁 Files: Updated `.specify/memory/constitution.md` (added 19 lines for Rule 14 + updated metadata)
- 🔁 Next prompts: Monitor Rule 14 enforcement during next /sp.implement execution; consider adding enforcement addendum if user provides complete text; potentially create ADR for commit workflow standardization
- 🧠 Reflection: Rule 14 complements Rule 9 (commit message format) by adding temporal trigger (immediately after /sp.implement) and interactive confirmation mechanism. This prevents both forgotten commits and premature commits, while maintaining traceability through structured message format.

## Evaluation notes (flywheel)

- Failure modes observed: None during amendment. Potential risk: Rule 14 may conflict with existing git hooks or CI/CD workflows that expect different commit message formats; monitoring needed during first /sp.implement execution
- Graders run and results (PASS/FAIL): N/A (constitutional amendment baseline)
- Prompt variant (if applicable): User provided exact wording for Rule 14 in imperative form; assistant added rationale section for consistency with existing constitutional structure
- Next experiment (smallest change to try): Execute /sp.implement workflow to validate Rule 14 triggers correctly; observe if dropdown UX is clear and if commit message format satisfies both Rule 9 and Rule 14 requirements simultaneously
