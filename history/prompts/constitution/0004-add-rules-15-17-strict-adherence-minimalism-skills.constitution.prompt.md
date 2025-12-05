---
id: 0004
title: Add Rules 15-17 strict adherence minimalism skills
stage: constitution
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 002-part0-introduction
user: Alishba
command: /sp.constitution
labels: ["constitution", "rules", "prompt-adherence", "skills", "minimalism"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

update my constitution.md adding my new instructions and requirements i need to specify that my agent will not write or add features by itself which i haven't mentioned in my prompt , it has to strictly stick to my given instruction and genearte all files according to that

I am a beginner and i am not adding images video in my book at this point so remove any if instruction related to image are there.

Mention to invoke related skills present in skill.md while writing book.

Mention to stay smart and minimalistic avoiding hallucunaions and achieving goal seamlessly.

## Response snapshot

Updated constitution.md from v1.2.0 to v1.3.0 (MINOR version bump) with three new rules:

**Rule 15: Strict Prompt Adherence - No Unauthorized Features**
Enforces that the agent must NEVER add features, content, or enhancements not explicitly requested in the prompt or specification.

**Rule 16: Skill Invocation Requirement for Book Content**
Mandates invoking the `professional-author` skill before writing any book content to ensure pedagogical standards are met.

**Rule 17: Smart Minimalism and Hallucination Prevention**
Requires ruthless efficiency, verified facts only, and stopping for clarification when information cannot be verified.

Also removed all image/video requirements from Rule 4 and deleted the commented "Image and Media Standards" section entirely.

## Outcome

- ✅ Impact: Added 3 critical rules enforcing prompt adherence, skill usage, and factual accuracy; removed beginner-irrelevant image requirements
- 🧪 Tests: Constitution validation (17 rules present, version incremented, no placeholder tokens remaining)
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Enforce Rules 15-17 in /sp.implement workflow; update agent instructions
- 🧠 Reflection: Constitution now explicitly prevents scope creep and hallucinations while requiring skill-based book authoring

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Manual validation PASS (all placeholders filled, version updated, rules coherent)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Test Rule 16 enforcement in next /sp.implement for book content
