# 📚 RAG Foundations — Short Notes

## 🔹 What We Covered
- Ran open-source LLMs using **Ollama**
- Previewed **embeddings** (text → numbers representing meaning)
- Introduced **RAG (Retrieval-Augmented Generation)** concept

---

## ❗ Why LLMs Alone Are Not Enough
- **Knowledge Cutoff** → No access to latest info  
- **No Private Data** → Cannot see company/internal documents  
- **Hallucination** → Confident but incorrect answers  
- **Context Limit** → Cannot handle very large documents  

👉 LLM = like a student trained on old public data

---

## 🔍 What Is RAG?
**Definition:**  
RAG = Retrieve relevant data → Add to prompt → Generate answer  

**Simple Idea:**  
📖 *Search first, then speak*

---

## 🧠 RAG Components

| Part        | Role |
|------------|------|
| Retriever  | Finds relevant documents |
| Generator  | LLM that writes answer |
| Grounding  | Forces answer to stick to provided context |

---

## 🔄 Five-Step RAG Flow

1. **Ingest** → Load documents (PDFs, web, etc.)
2. **Prepare** → Chunk + create embeddings
3. **Retrieve** → Find relevant chunks
4. **Augment** → Add chunks to prompt
5. **Generate** → LLM produces answer

---

## ⚖️ Without vs With Context

| Scenario        | Result |
|----------------|--------|
| Without context | Model guesses (may be wrong) |
| With context    | Accurate, grounded answer |

👉 Key Prompt Rule:

Answer only using the provided context.
If not found, say "Not in context."


---

## 🆚 RAG vs Fine-Tuning

| Feature        | RAG | Fine-Tuning |
|---------------|-----|------------|
| Updates info   | ✅ Easy | ❌ Hard |
| Uses documents| ✅ Yes | ❌ No |
| Changes model | ❌ No | ✅ Yes |

👉 RAG = bring the book  
👉 Fine-tuning = memorize the book  

---

## 🔢 Embeddings (Core Idea)

- Text → Vector (list of numbers)
- Similar meaning → vectors are closer

👉 Example:
- "refund policy" ≈ "return product" ✅  
- "refund policy" ≠ "exam viva" ❌  

---

## 💻 Code Concept (Embeddings)

- Load model: `SentenceTransformer`
- Convert text: `model.encode()`
- Output: vector (e.g., 384 numbers)

---

## 🔗 How This Leads to RAG

1. Convert text → embeddings  
2. Store in **vector database**  
3. Search similar vectors  
4. Retrieve relevant text  
5. Send to LLM → generate answer  

---

## 🧪 Key Learning

👉 RAG automates:

Embed → Store → Search → Add Context → Generate


---

## 📝 One-Line Summary
**RAG gives LLMs access to your own knowledge by retrieving relevant documents before generating answers.**