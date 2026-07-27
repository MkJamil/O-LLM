# Week 4 - Day 2 Task: Execution and Comparison of Claude Skills

## Executive Summary
This report documents the hands-on execution and comparative analysis of official Claude Skills (`/canvas-design` and `/web-artifacts-builder`) using both identical and varied prompt inputs. The goal is to observe how skill instructions alter Claude's execution behavior, output formats, and scope handling.

---

## Task Execution & Methodology

### Tested Skills
1. **`/canvas-design`**: Anthropic skill engineered for graphic design hierarchy, layout aesthetics, visual presentations, and copy structure.
2. **`/web-artifacts-builder`**: Anthropic skill engineered for interactive, multi-component web application building (React, Vite, shadcn, state management).

---

## Scenario Analysis

### Scenario A: Execution on Identical Input
* **Shared Input Prompt:**  
  > *"Please create a simple landing page hero section for a product called 'RefactorAI'."*

#### 1. Output & Behavior — `/canvas-design`
* **Trigger Mechanism:** Triggered via explicit `/canvas-design` slash command.
* **Observed Execution:** The skill applied deliberate visual design choices (Space Grotesk headline typography, JetBrains Mono code labels, editor-navy background with amber CTAs).
* **Generated Output:** A standalone visual HTML artifact featuring stylized headline copy (*"Tangled code, refactored on sight."*), action buttons, and an animated code transformation preview (`billing_service.py`).

#### 2. Output & Behavior — `/web-artifacts-builder`
* **Trigger Mechanism:** Triggered via explicit `/web-artifacts-builder` slash command.
* **Observed Execution:** Upon inspecting the prompt complexity against its internal system instructions (designed for full React + Vite + shadcn pipelines), the skill recognized that a single hero section did not warrant a complex multi-file React architecture.
* **Generated Output:** A meta-cognitive evaluation explaining that the task was better suited for a standalone HTML artifact (as created in the prior turn), asking if the user specifically wanted a full React project setup instead.

---

### Scenario B: Behavioral Variance Across Input Types

| Feature / Dimension | Standard / Single-Asset Input | Complex / Multi-Component Input |
| :--- | :--- | :--- |
| **`/canvas-design` Behavior** | Directly outputs structured HTML/CSS visual mockups with curated typography and visual hierarchy. | Focuses on layout grid breakdown, design system consistency, and visual branding assets. |
| **`/web-artifacts-builder` Behavior** | Evaluates scope first; flags potential over-engineering for simple single-section prompts. | Dynamically constructs interactive React components with dynamic state, routing, and UI libraries. |

---

## Comparative Analysis Matrix

| Comparison Metric | `/canvas-design` | `/web-artifacts-builder` |
| :--- | :--- | :--- |
| **Primary Domain** | Graphic composition, styling, typography, and visual assets. | Software engineering, interactive web applications, and state logic. |
| **Response Strategy** | Direct code/visual asset generation. | Scope evaluation $\rightarrow$ Interactive component pipeline setup. |
| **Scope Management** | Accepts small layouts and outputs instant visual renditions. | Protects context by avoiding over-engineering simple single-section prompts. |
| **Output Type** | Polished visual layout preview. | Interactive frontend artifact / modular React codebase. |

---

## Key Findings & Deliverable Outcomes

1. **Persona & Priority Shift:** Applying a specific skill fundamentally alters Claude's core persona—transforming it from a **visual designer** focused on brand aesthetics (`/canvas-design`) into a **systems architect** focused on component scope and pipeline fit (`/web-artifacts-builder`).
2. **Progressive Disclosure & Efficiency:** Skills do not merely append text; they enforce boundaries. `/web-artifacts-builder` prevented unnecessary context usage by evaluating whether a heavy framework pipeline was required before writing multi-file boilerplate.
3. **Task Alignment:** Selecting the right skill for a given task ensures optimal token usage and avoids over- or under-engineered solutions.