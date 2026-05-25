# GenAI & Agentic Systems Lab 🤖

This repository serves as a centralized hub for my technical implementation of **Module 3: GenAI & Agents** during my fellowship in Agentic Systems and Design through **iHUB DivyaSampark at IIT Roorkee**.

The goal of this project is to move beyond simple prompting into the engineering of autonomous, reliable, and production-ready AI workflows.

## 🚀 Module Overview

This lab documents the progression from LLM fundamentals to complex agentic orchestration, focusing on four core pillars:
1. **Foundational GenAI:** Tokens, context windows, and probabilistic generation.
2. **Retrieval-Augmented Generation (RAG):** Vector search, embeddings, and hybrid retrieval.
3. **Agentic Autonomy:** Planning, memory, control flow (Nodes/Transitions), and tool-use.
4. **AI Engineering:** Pydantic validation, structured outputs, and AI-native development (Cursor/Linting).

---

## 🛠️ Tech Stack & Tools

* **Orchestration:** LangGraph / LangChain
* **LLMs:** Ollama (Local), Hugging Face Ecosystem
* **Data & Validation:** Pydantic (JSON Schema Contracts), Vector Databases
* **Backend Integration:** FastAPI, PostgreSQL
* **AI-Native Dev:** Cursor, Linting, & Automated Testing

---

## 📂 Repository Structure

The learning journey is organized into structured phases:

### 01. LLM Foundations & Prompt Engineering
* Implementation of Zero-shot, Few-shot, and **Chain of Thought (CoT)** prompting.
* System vs. User prompt architectural design.
* Local LLM deployment via **Ollama**.

### 02. RAG Architectures (The "Snack App")
* Building end-to-end RAG pipelines.
* **Embeddings & Vector Search** optimization.
* Multimodal pipelines (Speech-to-Text and Text-to-Speech integration).

### 03. Agentic Patterns & Autonomy
* **Memory & State Management:** Designing persistent agent states.
* **Control Flow:** Constructing agent graphs using nodes and transitions.
* **Tool Orchestration:** Integrating agents with external APIs and reasoning loops.

### 04. Reliability & Guardrails
* **Output Parsing:** Ensuring reliable integration via JSON schema contracts.
* **Safety:** Prompt injection prevention and toxicity detection.
* **Human-in-the-loop:** Implementing gates for supervised autonomy.

---

## 🧪 Featured Implementations

### **RAG Snack App**
A lightweight application demonstrating the retrieval of domain-specific data to augment LLM responses, focusing on low-latency vector search.

### **Agentic Reasoning Loop**
A demonstration of an agent capable of using tools, managing its own memory, and correcting its own mistakes through a structured reasoning loop.

---

## 📈 Engineering Standards

In line with my focus on **Software Engineering**, this repo follows strict development practices:
* **Type Safety:** Heavy use of Pydantic for data integrity.
* **Observability:** Implementing tracing for reasoning steps.
* **Testing:** Unit tests for RAG retrieval accuracy and tool-calling reliability.

---

## 🎓 About the Program
This work is part of the **Certification Program in Agentic Systems and Design** at **IIT Roorkee**. It reflects my transition from traditional Backend Engineering into **Agentic AI Systems Engineering**.

---

## 🔗 Connect with Me
* **Portfolio:** [YS-Pundir on GitHub](https://github.com/YS-Pundir)
* **Current Focus:** Building scalable AI infrastructure and autonomous workflows.
