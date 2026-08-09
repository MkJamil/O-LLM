# RefactorAI — AI-Powered Enterprise Codebase Modernization Platform

RefactorAI is a high-performance web platform designed to analyze, refactor, and optimize multi-file enterprise codebases using advanced multi-agent LLM orchestration. Built for speed, security, and developer clarity, RefactorAI transforms legacy, tightly coupled, or unoptimized code into production-ready software.

---

## ✨ Key Features

* 🤖 **Multi-Agent Orchestration Loop:** Assign dedicated LLM agents to targeted files or directories with granular file selection toggles.
* 📁 **Smart Workspace File Tree:** Local directory picker and GitHub integration with automatic file filtering to keep your workspace focused purely on source code.
* ⚡ **Token Compression & Auto-Batching:** Client-side comment stripping and dynamic request chunking to maximize throughput and bypass rate limits (TPM).
* 🛡️ **Rate-Limit Backoff & Failover:** Graceful 429 backoff handling and multi-provider fallback support.
* 📊 **Structured Architectural Audits:** Clear, structured output detailing:
  1. **Code Purpose & Flaws Analysis** (Identified anti-patterns, security risks, and performance bottlenecks).
  2. **Production-Ready Code** (Complete, un-truncated refactored code).
  3. **Verification & Complexity Metrics** (Testing steps and Big-O Time/Space complexity).
* 📄 **Executive PDF Audit Export:** One-click generation of native vector PDF audit reports for executive reviews.

---

## 🛠️ Supported Languages

* **Core Languages:** Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, Scala, SQL, Shell/Bash, HTML, CSS.

---

## 🚀 Quick Start

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/RefactorAI.git](https://github.com/your-username/RefactorAI.git)
   cd RefactorAI
   ```

2. **Open the Application:**
   Open `index.html` directly in any modern browser (Chrome, Edge, Firefox, Safari). No backend build step required.

3. **Configure API Key:**
   Select your preferred provider from the top dropdown menu and paste your API key:
   * **Google AI Studio** (Gemini)
   * **Groq**
   * **OpenRouter**
   * **OpenAI / Anthropic**

4. **Refactor Code:**
   * Load local files or paste code snippets into the main editor.
   * Toggle workspace checkboxes to select files for Multi-Agent processing.
   * Click **Run RefactorAI**.

---

## 🏗️ Architecture & Stack

* **Frontend:** HTML5, Tailwind CSS, Vanilla JS (ES6+)
* **State & Scope Management:** Dynamic AST gathering with checkbox workspace synchronization
* **Export Engine:** Native Browser Print Vector PDF Renderer

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
