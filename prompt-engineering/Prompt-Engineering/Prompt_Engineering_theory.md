# 🚀 Prompt Engineering — 1-Page Revision Sheet

---

## 🧩 1. System Prompt vs User Prompt

**System Prompt (Hidden Rules)**
- Defines **role, behavior, limits**
- Persistent across session
- Controls AI output style & boundaries

**User Prompt (Live Input)**
- Real-time instructions from user

👉 AI = *User Prompt filtered through System Prompt*

---

### 🔑 3 Core Ingredients of System Prompt

| Ingredient | Purpose | Example |
|-----------|--------|--------|
| Persona | Identity & role | "You are a patient mentor..." |
| Scope | Allowed topics | "Only answer AI/ML questions" |
| Tone & Rules | Style + constraints | "No jargon, use simple analogies" |

---

## 🎯 2. Zero-Shot vs Few-Shot Prompting

**Zero-Shot**
- No examples
- Uses pre-trained knowledge
- ✅ Best for simple tasks

**Few-Shot**
- 1–5 examples included
- Improves consistency & format
- ✅ Best for complex / structured tasks

---

## 🧠 3. Chain-of-Thought (CoT) Prompting

**Definition**
- Forces model to show **step-by-step reasoning**

**Why it works**
- Reduces logical errors
- Improves math & multi-step tasks

**Types**
- **Zero-Shot CoT:**  
  → "Let's think step by step"
- **Few-Shot CoT:**  
  → Provide solved example with reasoning

---

## 🏗️ 4. Prompt Templates (Structured Prompts)

**Goal:** Consistent, programmatic outputs


Role → Who the AI is
Task → What to do
Instructions → Step-by-step actions
Constraints → Limits (no jargon, etc.)
Output Form → Exact format


👉 Separates **data vs rules** → more reliable outputs

---

## 🔍 5. Self-Correction Prompting

**Definition**
- AI evaluates & fixes its own output

**3-Step Flow (must be explicit)**


[GENERATE] → [CRITIQUE] → [REWRITE]


- Generate answer
- Check against criteria
- Fix all issues

👉 Prevents shallow or incorrect outputs

---

## 🔁 6. Iterative Prompting

**Definition**
- Multi-step refinement through conversation

**Cycle**


DRAFT → REVIEW → REFINE


- Draft: initial output
- Review: find biggest flaw
- Refine: fix with targeted prompt

👉 Used to build **production-ready prompts**

---

## 🧠 Quick Mental Model

- System Prompt = **Rules**
- User Prompt = **Input**
- Few-shot = **Examples = control**
- CoT = **Reasoning boost**
- Templates = **Structure**
- Self-correct = **QA layer**
- Iteration = **Refinement loop**

---