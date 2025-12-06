# Tasks: Part 1 - The Robotic Nervous System (ROS 2)

**Feature**: 004-ros2-nervous-system
**Branch**: `004-ros2-nervous-system`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

**Content Overview**: Create Part 1 of the Physical AI textbook focusing on ROS 2 as the "nervous system" of robots. This includes 4 chapters (ROS 2 fundamentals, robot visualization, package development, AI-agent integration), an overview document, and a self-assessment module.

---

## Phase 1: Setup

**Goal**: Initialize content authoring environment and load research artifacts

- [X] T001 Verify research.md contains all ROS 2 Humble facts with source URLs
- [X] T002 Verify SKILL.md professional-author guidelines accessible at .claude/skills/professional-author/SKILL.md
- [X] T003 Verify Docusaurus build succeeds (npm run build exits 0)

---

## Phase 2: Foundational Tasks

**Goal**: Establish shared resources needed by all user stories

- [X] T004 Verify Part 1 category link in sidebars.js points to part1-introduction.mdx

---

## Phase 3: User Story 1 - ROS 2 Architecture Fundamentals (P1)

**Story Goal**: Enable beginner AI practitioners to understand ROS 2 architecture and create publisher/subscriber nodes

**Independent Test**: Reader can create a simple publisher/subscriber pair and verify messages flow between nodes

**Files Created**:
- docs/part1-module1/chapter-3-ros-2-crash-course.mdx
- docs/part1-module1/part1-introduction.mdx

### Implementation Tasks

- [X] T005 [US1] Invoke professional-author skill per Rule 15
- [X] T006 [US1] Create docs/part1-module1/part1-introduction.mdx with valid YAML frontmatter
- [X] T007 [US1] Write Learning Objectives section (3-5 actionable objectives)
- [X] T008 [US1] Write Why This Matters in 2025 section (ROS 2 as robot nervous system)
- [X] T009 [US1] Write ROS 2 architecture definition in plain English (simple then technical)
- [X] T010 [US1] Write 2025 landscape section (ROS 2 Humble, nodes, topics, services, actions with URLs)
- [X] T011 [P] [US1] Create Mermaid diagram: ROS 2 architecture overview (nodes, topics, services)
- [X] T012 [P] [US1] Create Mermaid diagram: Communication patterns (publisher/subscriber, client/service)
- [X] T013 [US1] Write rclpy basics section with minimal code examples (under 50 lines)
- [X] T014 [US1] Write hands-on publisher/subscriber example (talker/listener demo)
- [X] T015 [US1] Write common mistakes section (node naming, QoS mismatches, etc.)
- [X] T016 [US1] Write What's Next section teasing Chapter 4
- [X] T017 [US1] Validate: 3800-4200 words, 2+ diagrams, no forbidden words, all terms defined

---

## Phase 4: User Story 2 - Robot Visualization and Description (P2)

**Story Goal**: Enable readers to create and visualize robot models using URDF/Xacro in RViz2

**Independent Test**: Reader can create a simple robot model and visualize it in RViz2, seeing joint states and transformations in real-time

**Files Created**: docs/part1-module1/chapter-4-talking-to-robots.mdx

### Implementation Tasks

- [X] T018 [US2] Invoke professional-author skill per Rule 15
- [X] T019 [US2] Create chapter-4-talking-to-robots.mdx with valid YAML frontmatter
- [X] T020 [US2] Write Learning Objectives section (3-5 actionable objectives)
- [X] T021 [US2] Write Why This Matters in 2025 section (visualization for understanding)
- [X] T022 [US2] Write URDF/Xacro definition in plain English (simple then technical)
- [X] T023 [US2] Write URDF/Xacro examples section (simple arm/leg models for humanoid robots)
- [X] T024 [P] [US2] Create Mermaid diagram: URDF kinematic chain (links and joints)
- [X] T025 [P] [US2] Create Mermaid diagram: Robot model hierarchy (URDF → joint_state_publisher → robot_state_publisher → RViz2)
- [X] T026 [US2] Write joint state publisher and robot state publisher section
- [X] T027 [US2] Write RViz2 visualization section (joint states, TF frames)
- [X] T028 [US2] Write hands-on example: creating and visualizing a simple humanoid model
- [X] T029 [US2] Write common mistakes section (malformed URDF, TF tree issues)
- [X] T030 [US2] Write What's Next section teasing Chapter 5
- [X] T031 [US2] Validate: 3800-4200 words, 2+ diagrams, no forbidden words, all terms defined

---

## Phase 5: User Story 3 - Package Development and Workspace Management (P3)

**Story Goal**: Enable readers to create and manage real workspaces with colcon, launch files, and parameters

**Independent Test**: Reader can create a functional ROS 2 package with launch files and parameters, and successfully build and run it using colcon

**Files Created**: docs/part1-module1/chapter-5-building-real-packages.mdx

### Implementation Tasks

- [X] T032 [US3] Invoke professional-author skill per Rule 15
- [X] T033 [US3] Create chapter-5-building-real-packages.mdx with valid YAML frontmatter
- [X] T034 [US3] Write Learning Objectives section (3-5 actionable objectives)
- [X] T035 [US3] Write Why This Matters in 2025 section (professional ROS 2 development)
- [X] T036 [US3] Write colcon workspace definition in plain English (simple then technical)
- [X] T037 [US3] Write colcon workspace creation section (from scratch)
- [X] T038 [P] [US3] Create Mermaid diagram: Package structure (workspace/src/packages)
- [X] T039 [P] [US3] Create Mermaid diagram: Build process (colcon build → install → run)
- [X] T040 [US3] Write Python and C++ package templates section
- [X] T041 [US3] Write launch files and parameter management section (YAML configs)
- [X] T042 [US3] Write hands-on example: creating a complete workspace with launch files
- [X] T043 [US3] Write common mistakes section (package.xml issues, launch file errors)
- [X] T044 [US3] Write What's Next section teasing Chapter 6
- [X] T045 [US3] Validate: 3800-4200 words, 2+ diagrams, no forbidden words, all terms defined

---

## Phase 6: User Story 4 - AI-Agent to ROS 2 Bridge (P4)

**Story Goal**: Enable AI practitioners to connect Python AI agents to ROS 2 for sending commands and reading sensors

**Independent Test**: Reader can create a Python script that reads sensor data from ROS 2 topics and sends commands back to control a robot, demonstrating the AI-robot connection

**Files Created**: docs/part1-module1/chapter-6-bridging-ai-agents-to-ros.mdx

### Implementation Tasks

- [X] T046 [US4] Invoke professional-author skill per Rule 15
- [X] T047 [US4] Create chapter-6-bridging-ai-agents-to-ros.mdx with valid YAML frontmatter
- [X] T048 [US4] Write Learning Objectives section (3-5 actionable objectives)
- [X] T049 [US4] Write Why This Matters in 2025 section (AI to physical action bridge)
- [X] T050 [US4] Write AI-agent to ROS 2 integration definition in plain English (simple then technical)
- [X] T051 [US4] Write Python agent → ROS 2 node conversion section (20 lines example)
- [X] T052 [P] [US4] Create Mermaid diagram: AI-ROS integration (sensor data → AI agent → commands → robot)
- [X] T053 [P] [US4] Create Mermaid diagram: Message flow (Twist messages, JointState messages)
- [X] T054 [US4] Write velocity commands section (Twist messages)
- [X] T055 [US4] Write sensor data reading section (JointState into agent loop)
- [X] T056 [US4] Write hands-on example: connecting a simple AI agent to ROS 2
- [X] T057 [US4] Write common mistakes section (timing issues, data conversion)
- [X] T058 [US4] Write What's Next section teasing Part 2 (ROS 2 Navigation)
- [X] T059 [US4] Validate: 3800-4200 words, 2+ diagrams, no forbidden words, all terms defined

---

## Phase 7: User Story 5 - Self-Assessment and Validation (P5)

**Story Goal**: Enable learners to validate their understanding through interactive assessments

**Independent Test**: Reader completes the interactive self-assessment with 80%+ score, demonstrating mastery of the material

**Files Created**: docs/part1-module1/part-1-self-assessment.mdx

### Implementation Tasks

- [ ] T060 [US5] Invoke professional-author skill per Rule 15
- [ ] T061 [US5] Create part-1-self-assessment.mdx with valid YAML frontmatter
- [ ] T062 [US5] Write introduction section (purpose and instructions for self-assessment)
- [ ] T063 [US5] Generate 10 high-quality MCQs from Chapters 3-6 content
- [ ] T064 [US5] Generate short code-fix questions from Chapters 3-6 examples
- [ ] T065 [US5] Write interactive exam flow section ("Start Quiz" → one question per page → "Next" button)
- [ ] T066 [US5] Write instant results and detailed explanations section
- [ ] T067 [US5] Write score-based guidance section (0–4 → review, 5–8 → good progress, 9–10 → ready for Module 2)
- [ ] T068 [US5] Validate: Interactive components work, explanations provided, score guidance clear

---

## Phase 8: Polish & Validation

**Goal**: Cross-cutting validation and quality checks

- [ ] T069 [P] Run npm run build (verify exit code 0)
- [ ] T070 [P] Verify Part 1 sidebar category clickable
- [ ] T071 [P] Language check: no obviously/simply/just in main content
- [ ] T072 Validate total Mermaid diagrams >= 10 (2 per chapter × 5 chapters)
- [ ] T073 Visual formatting check vs SKILL.md standards
- [ ] T074 Manual browser test: navigation, diagram rendering, content flow
- [ ] T075 Validate word count: ~18,000 total (2k overview + 4k × 4 chapters + assessment)

---

## Dependencies & Parallel Execution

**Story Order**: Setup → Foundational → US1 || US2 || US3 || US4 → US5 → Polish

**Parallel in Phase 3**: T011, T012 (after T010)
**Parallel in Phase 4**: T024, T025 (after T023)
**Parallel in Phase 5**: T038, T039 (after T037)
**Parallel in Phase 6**: T052, T053 (after T051)
**Parallel in Phase 8**: T069, T070, T071

All user stories INDEPENDENT - can implement/test/deploy separately

---

## Summary

**Total**: 75 tasks
**US1**: 12 tasks | **US2**: 12 tasks | **US3**: 12 tasks | **US4**: 12 tasks | **US5**: 7 tasks
**Setup/Foundational**: 4 | **Polish**: 7 tasks
**Parallel opportunities**: 8 tasks

**MVP**: US1 only (16 tasks) delivers core ROS 2 fundamentals
**Incremental**: US1 → US2 → US3 → US4 → US5 → Polish
**Validation**: All tasks follow checklist format ✅

**Next**: `/sp.implement` to execute using professional-author skill