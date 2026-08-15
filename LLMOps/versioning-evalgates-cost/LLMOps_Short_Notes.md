# LLMOps — Short Notes

## 1. LLMOps & Evaluation

**LLMOps** = managing the full lifecycle of LLM applications in production:
- Development → deployment → evaluation → monitoring → improvement
- Prompt/model versioning
- RAG management
- Observability & tracing
- Deployment & scaling
- Latency & cost tracking
- Guardrails & safety
- Feedback loops

**Key idea:** Evaluation is continuous, not a one-time task. fileciteturn0file0L14-L17

---

## 2. Classification Evaluation

Classification examples:
- Positive vs. negative sentiment
- Email categories
- Support priority levels
- Emotion detection

### Confusion Matrix
Compares **actual values vs. predicted values**.

- **False Positive (FP):** predicted positive, actually negative
- **False Negative (FN):** predicted negative, actually positive
- The more costly error depends on the real-world application.

### F1 Score
- Standard classification metric.
- Calculated per class.
- Useful for balancing precision and recall.

**Remember:** Do not automatically assume FP and FN have equal costs. fileciteturn0file0L29-L40

---

## 3. Audio → AI Pipeline

For voice systems:

**Audio → ASR/STT → text/representation → LLM/classifier → TTS → audio**

- **ASR/STT:** converts speech into text/representation.
- **TTS:** converts generated text back into speech.
- Plain transcription captures words but may lose tone.
- Tone-aware processing additionally uses acoustic features for emotion detection. fileciteturn0file0L42-L49

### Gold Set
A **gold example/set** is a curated, held-out evaluation dataset used to measure model performance. fileciteturn0file0L51-L51

---

## 4. Generation Evaluation

Two main cases:

### Ground Truth Exists
Compare generated output with the expected output.

Example:
- **BERTScore:** compares semantic representations/embeddings of predicted and actual text.

### No Ground Truth
Use **LLM-as-a-Judge**:
1. First LLM generates the answer.
2. Second LLM acts as the judge.
3. Judge scores the answer, e.g. **1–5**.
4. Judge criteria are defined through its system prompt. fileciteturn0file0L53-L59

---

## 5. RAG Evaluation — The RAG Triad

RAG is evaluated using:

### 1. Context Relevance
**Is the retrieved context relevant to the user's question?**

### 2. Groundedness
**Is the answer actually supported by the retrieved context?**

### 3. Answer Relevance
**Does the generated answer actually answer the question?** fileciteturn0file0L60-L66

### Important
**Groundedness is non-negotiable.**

The model should not use its pretrained knowledge to fill missing information. If the answer is not supported by retrieved context, it should say **"I don't know."** fileciteturn0file0L68-L70

---

## 6. Diagnosing a Bad RAG Pipeline

When a RAG score is low:

### Context Relevance Low
Investigate:
- Chunking strategy
- Embedding model
- Vector DB metadata
- Number of retrieved chunks

→ **Retrieval problem**

### Groundedness Low
Investigate:
- System prompt
- Generation settings
- Context passed to the LLM

→ **Generation/grounding problem**

### Answer Relevance Low
Check:
- Retrieval
- Generation
- Both stages

### Practical Debugging Order
**Context relevance → Groundedness → Answer relevance**

Fix retrieval first because bad retrieval affects everything downstream. fileciteturn0file0L72-L103

---

## 7. LLM-as-a-Judge for RAG

Typical flow:

```text
User Query
    ↓
Retriever
    ↓
Context
    ↓
LLM
    ↓
Generated Answer
    ↓
Judge Model
    ↓
Evaluation Score
```

Separate judges can evaluate:
- Groundedness
- Relevance

The judge receives the **query + context + generated response** and produces a score based on its evaluation prompt. fileciteturn0file0L111-L115

### Golden Set for RAG
- Curated by the team/domain experts.
- Should contain different question types.
- Does not necessarily require pre-written correct answers.
- Questions are evaluated through retrieval + generation + judge models. fileciteturn0file0L117-L117

---

## 8. Offline vs Online Evaluation

| Type | Meaning |
|---|---|
| **Offline** | Evaluation before/outside production using a fixed test set |
| **Online** | Evaluation using live production traffic |

Online evaluation usually samples a portion of traffic rather than evaluating every request. fileciteturn0file0L119-L122

---

## 9. AI Gateway

An **AI Gateway** sits between applications and LLM APIs.

### Main Purpose
**Intelligent model routing + load distribution + fallback**

Instead of sending every request to one model:

```text
                 ┌── Cheap/Fast Model
                 │
User → Gateway ──┼── Powerful Model
                 │
                 └── Other Provider/Model
```

### Routing Example
- Simple/urgent query → cheap, low-latency model
- Complex/high-stakes query → powerful model
- Policy/general query → appropriate model tier

### Benefits
- Reduces rate-limit errors such as **HTTP 429**
- Distributes traffic
- Controls cost
- Supports multiple models/providers
- Enables dynamic fallback routing

**Key concept:** AI Gateway ≈ **classifier + load balancer + model-aware routing**. fileciteturn0file0L138-L151

---

## 10. Semantic Caching

**Semantic cache** stores previous **question-answer pairs as embeddings**.

Flow:

```text
New Query
   ↓
Semantic Cache
   ↓
Similar Query Found?
  ↙        ↘
 Yes        No
 ↓           ↓
Cached      Full RAG
Answer      Pipeline
```

### Good For
- Repeated
- Stable
- FAQ-style queries

Example:
- Return policy
- Cancellation policy

### Bad For
Dynamic information such as:
- Live order status
- Frequently changing data

### Benefits
- Avoids retrieval + generation for cache hits
- Reduces latency
- Reduces LLM/API load
- Helps reduce rate-limit errors

**Key idea:** Semantic caching improves **latency and load**, not answer quality directly. fileciteturn0file0L155-L161

---

## 11. AI Gateway vs Semantic Cache

| Component | Main Job |
|---|---|
| **Semantic Cache** | Avoids unnecessary LLM calls |
| **AI Gateway** | Distributes required LLM calls across models/providers |

### Together

```text
User Request
     ↓
Semantic Cache
   ↙       ↘
 HIT       MISS
 ↓          ↓
Answer   AI Gateway
            ↓
      Model Routing
       ↙    ↓    ↘
    Model A Model B Model C
```

**Simple rule:**
- Cache = **reduce load**
- Gateway = **distribute load** fileciteturn0file0L161-L163

---

## 12. Quick Revision

### Evaluation
**Classification → Confusion Matrix + F1**

**Generation with ground truth → Compare against expected output**

**Generation without ground truth → LLM-as-a-Judge**

**RAG → Context Relevance + Groundedness + Answer Relevance**

### RAG Debugging
**Bad retrieval → fix context relevance**

**Unsupported answer → fix groundedness**

**Poor answer → inspect retrieval + generation**

### Production LLMOps
**LLMOps → Evaluation + Monitoring + Versioning + Observability + Scaling + Cost + Safety**

**AI Gateway → intelligent routing**

**Semantic Cache → reuse semantically similar previous answers**

### Most Important Takeaways
1. Evaluation is continuous.
2. FP/FN costs depend on the application.
3. Groundedness is essential in RAG.
4. Fix retrieval problems before generation problems.
5. LLM-as-a-Judge is useful when fixed ground truth is unavailable.
6. AI gateways distribute LLM traffic intelligently.
7. Semantic caching reduces repeated LLM work.
8. AI Gateway and semantic caching solve different but complementary scaling problems.
