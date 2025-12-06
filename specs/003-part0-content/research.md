# Research: Part 0 Content - 2025 Physical AI Landscape & SDD Methodology

**Feature**: 003-part0-content  
**Research Date**: 2025-12-06  
**Purpose**: Gather verified facts for Chapter 0.1 (Physical AI significance) and Chapter 0.2 (SDD methodology)

---

## 1. 2025 Physical AI Landscape

### Definition

**Physical AI**: Models that understand and interact with the real world using motor skills, housed in autonomous machines (robots, self-driving vehicles). Enables systems to perceive, reason, and act in real-world environments.

**Sources**:
- https://www.nvidia.com/en-us/glossary/generative-physical-ai/
- https://www.weforum.org/stories/2025/09/what-is-physical-ai-changing-manufacturing/

### Figure AI (2025)

- **Helix Model (Feb 2025)**: Vision-Language-Action model, picks thousands of novel objects
- **BotQ Facility (Mar 15, 2025)**: 12,000 humanoids/year production capacity
- **Figure 03 (Oct 9, 2025)**: Third-gen humanoid, TIME Best Inventions 2025, learns from humans
- **Demo**: Figure 02 autonomously folded towels (no remote control)

**Sources**: https://techcrunch.com/2025/02/20/figures-humanoid-robot-takes-voice-orders-to-help-around-the-house/

### Tesla Optimus (2025)

- **Production**: Target 5,000 units (actual: few hundred by July 2025)
- **Tech Progress**: Smooth running demo (Dec 2, 2025), improved gait
- **Challenges**: Hand dexterity, rare earth metal export restrictions
- **Strategy**: Musk claims 80% of Tesla future value from Optimus
- **Pricing**: 0k-0k at scale

**Sources**: https://standardbots.com/blog/tesla-robot

### Boston Dynamics Atlas (2025)

- **Transition**: All-electric design (2024), commercial focus under Hyundai
- **Atlas 2.0**: Enhanced 2D/3D vision, sensor fusion, adaptive decision-making
- **Partnership**: Toyota Research Institute for AI model testing
- **Platform**: NVIDIA Jetson Thor for multimodal AI

**Sources**: https://bostondynamics.com/atlas/

### Agility Robotics Digit (2025)

- **Status**: 2024 RBR50 Robot of Year, first humanoid in commercial deployment
- **Production**: 10,000 units/year, Amazon-backed
- **Capabilities**: AI vision for picking/placing thousands of boxes/shift

**Sources**: https://www.therobotreport.com/agility-robotics-announces-latest-advances-digit-humanoid-robot/

### 5 Opportunity Domains

1. **Manufacturing**: UR15 with NVIDIA tech, 20-30% faster cycles, 25% fewer errors
2. **Warehouse**: 1M robots, 300+ centers, 25% efficiency boost
3. **Humanoid Tasks**: Tesla/Figure for home and industrial tasks
4. **Agriculture**: Harvesting, crop monitoring, autonomous navigation
5. **Healthcare**: Patient assistance, eldercare, mobility support

**Market**: 2B → 24B by 2030. NVIDIA CEO (CES 2025): revolutionize 0T manufacturing/logistics

### 3 Unique Challenges vs Traditional AI

1. **Hardware-Software Integration**: Real-time control loops, mechanical failures, actuator coordination
2. **Real-World Unpredictability**: Chaotic environments, sim-to-real gap, object variations
3. **Safety Requirements**: Equipment damage, human injury risks, regulatory burden

---

## 2. SDD Benefits for Physical AI

### Definition

Spec-Driven Development: Define software behavior, constraints, interfaces before implementation. Specification is source of truth for humans and AI.

**Sources**: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/

### 2025 Status

Table stakes for AI-augmented engineering. 15+ platforms launched 2024-2025 (AWS Kiro, GitHub Spec Kit).

### 4 Benefits for Physical AI

1. **Prevents Integration Failures**: Specs define interfaces/constraints upfront, preventing hardware-software mismatches. Model-driven ROS: 11% of time vs code-centric.

2. **Reduces Debugging**: Clear validation criteria catch errors before expensive physical deployment. Less modification over lifecycle.

3. **Enables AI Code Generation**: AI generates ROS packages from specs in minutes vs hours manual setup.

4. **Improves Team Alignment**: Single source of truth for cross-disciplinary teams (mechanical, electrical, software, AI).

### When Use SDD vs Overkill

**Use**: Multi-team, complex systems, hardware integration, safety-critical, long-term, AI-assisted  
**Overkill**: Quick prototypes, single dev, simple scripts (<100 lines), educational basics

### Common Mistakes

1. Skipping specification (jumping to code)
2. Over-planning (analysis paralysis)
3. Vague requirements  
4. Not updating specifications

---

## 3. Formatting Standards

### MDX Frontmatter



### Heading Hierarchy

- H1: Chapter title (once)
- H2: Major sections
- H3: Subsections
- H4: Rare, deep sub-topics

### Concept Introduction Pattern

1. One-sentence simple definition
2. Precise technical explanation
3. Real-world analogy (optional)

---

## 4. Mermaid Diagram Patterns

### Resources

- https://mermaid.js.org/syntax/flowchart.html
- https://mermaid.live/ (testing)

### Flowchart (SDD Workflow)



### Comparison (Physical vs Traditional AI)



### Best Practices

- Max 5-7 nodes for beginners
- Full words, not abbreviations
- Consistent direction (LR or TD)
- 1-2 sentence context before/after

---

## Research Complete

**Status**: All unknowns resolved, Rules 2 & 16 satisfied  
**Next**: Phase 1 - data-model.md, contracts/, quickstart.md
