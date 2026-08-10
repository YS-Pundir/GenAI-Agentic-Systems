# 🚀 Module 3 — Agentic Systems (Session 1)
## ⚡ 1-Page Revision Sheet: GenAI & LLMs

---

## 🧱 1. Limits of Classical ML
- Works only on **structured/tabular data**
- Requires heavy **feature engineering**
- ❌ Cannot understand **context**
- ❌ Fails with **ambiguous words**
  - *"bank"* → multiple meanings

---

## 🧠 2. Neural Networks (Foundation of LLMs)
- Stack of layers learning **abstract patterns**

**Architecture:**
- Input → Hidden Layers → Output

**Key Components:**
- Weights (w), Biases (b)
- Deep Learning = more hidden layers

👉 LLMs = **billions of parameters**

---

## 📈 3. Evolution of LLMs


Word2Vec → RNNs → Transformer → GPT → ChatGPT


**Key Ideas:**
- **Word2Vec:** word embeddings (king - man + woman ≈ queen)
- **RNNs:** sequential but forget long context
- **Transformer:** attention → understands relationships
- **GPT:** predicts next token (pre-trained)
- **ChatGPT:** conversational AI

---

## 🔤 4. Tokens (Core Unit)
- Smallest unit: word / subword / symbol

**Example:**

unhappiness → ["un", "happi", "ness"]


**Rule:**
- 1 token ≈ 0.75 words

**Types:**
- Prompt tokens (input)
- Completion tokens (output)

---

## 🧩 5. Context Window (Memory Limit)
- Max tokens model can process

**Key Rule:**
- ❗ Beyond limit = **forgotten**

| Model        | Tokens  |
|--------------|--------|
| GPT-3.5      | 4K     |
| GPT-4        | 128K   |
| Gemini 1.5   | 1M     |

👉 Everything (prompt + history + output) shares this space

---

## 🎲 6. Text Generation & Temperature

**How it works:**
- Predicts **next token** step-by-step

**Temperature:**
- Low (0.1) → deterministic, safe (code, facts)
- High (1.5) → creative, diverse


Low ─────────────── High
Safe Creative
Repeatable Random


---

## ⚠️ 7. Hallucinations
- Confident but **wrong/fake outputs**

**Why?**
- Optimized for:
  - ✅ Plausibility (sounds right)
  - ❌ Truth (fact-checking)

👉 No built-in verification

---

## 🧠 Quick Mental Model
- LLM = **Next-token predictor + massive training**
- Works on **tokens, not words**
- Limited by **context window**
- Controlled by **temperature**
- Not a database → can **hallucinate**

---