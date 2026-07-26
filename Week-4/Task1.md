# Week 4 - Day 1 Task: Analysis of Claude Skills

## Overview
A Claude Skill is a modular set of instructions and guidelines packaged inside a `SKILL.md` file. It allows Claude to automatically apply domain-specific rules, formatting standards, and procedures without requiring the user to re-write complex prompt guidelines in every new chat.

---

## Skill Analysis

### 1. Code Review & Vulnerability Scanner
* **Problem Solved:** Developers often miss edge-case bugs, performance bottlenecks, or security vulnerabilities during manual self-reviews. Standard prompts often yield inconsistent feedback.
* **When It Triggers:** Triggered when a user provides code and uses phrases like *"Review this code,"* *"Check for security issues,"* or *"Scan for performance bugs."*
* **Core Function:** Analyzes code structure, highlights security flaws (e.g., SQL injections, unsafe inputs), checks compliance with style guidelines, and suggests optimized refactored versions.

---

### 2. Technical Documentation Generator
* **Problem Solved:** Technical documentation across software projects is frequently inconsistent, incomplete, or formatted differently depending on who wrote it.
* **When It Triggers:** Triggered when a user asks to *"Generate a README,"* *"Document this API endpoint,"* or *"Create technical docs for this file."*
* **Core Function:** Converts raw code files or functions into standardized Markdown documentation complete with usage examples, parameter descriptions, edge-case notes, and clean structural headers.

---

### 3. Unit Test Builder (Pytest / Jest)
* **Problem Solved:** Writing test boilerplate is repetitive and time-consuming. Developers frequently forget to write edge-case tests (e.g., handling null inputs, timeout errors, or boundary limits).
* **When It Triggers:** Triggered when a user provides a function or class and requests *"Write unit tests for this,"* *"Increase test coverage,"* or *"Create pytest cases."*
* **Core Function:** Reads the function logic and automatically generates a comprehensive test suite using the required testing framework, enforcing strict structure (Given-When-Then pattern) and covering both standard and edge-case inputs.

---

## Summary of the Skill Model Benefits
1. **Consistency:** Enforces identical output standards across team members and different chat sessions.
2. **Context Efficiency:** Keeps base context usage minimal by only loading specific instructions when a trigger word or matching intent is detected.
3. **Time Saving:** Replaces long, repetitive prompt engineering with automatic execution.