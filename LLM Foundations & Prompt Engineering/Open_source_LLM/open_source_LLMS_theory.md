### 💻 Hardware Constraints

- **Small Models (0.5B–3B)**  
  → Run smoothly on laptops

- **Large Models (70B+)**  
  → Require powerful GPUs (A100/H100)

---

## ⚡ 3. Groq Cloud API

- Ultra-fast cloud inference
- Runs open-source models (e.g., LLaMA 70B)

### Setup
- Get API key from console.groq.com
- Store securely (e.g., environment variables)

### Key Insight
- Uses **OpenAI-style API format**
👉 Same code structure across providers

---

## ⚠️ 4. Training Data Bias

LLMs reflect their training data

### Types of Bias
- **Geopolitical**  
  → China-trained vs US-trained models differ

- **Cultural**  
  → Humor, idioms, norms vary

👉 LLM ≠ neutral truth source

---

## 🧑‍💻 5. Implementation Pattern

### Core Idea
- Use **message list with roles**

---

### 🏠 Local (Ollama)

```python
from ollama import chat

response = chat(
    model="qwen2.5:0.5b",
    messages=[{"role": "user", "content": "Explain AI simply"}]
)

print(response["message"]["content"])
``` id="t9sdnk"

---

### ☁️ Cloud (Groq/OpenAI)

```python
from groq import Groq

client = Groq(api_key="YOUR_KEY")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are concise"},
        {"role": "user", "content": "What is RAG?"}
    ]
)

print(response.choices[0].message.content)
``` id="o2g8lb"

---

## 🎧 6. Multimodal AI (Beyond Text)

LLMs now handle multiple data types:

- **Vision** → image understanding  
- **Audio** → speech/text conversion  
- **Text** → traditional LLM tasks  

### Real Example
- Search photos:  
  → "Find sunset photo from plane"

👉 Combines vision + reasoning

---

## 🧠 Quick Mental Model

- Local = **privacy + free**
- Cloud = **speed + power**
- Ollama = **run models locally**
- Groq = **fast cloud inference**
- Bias = **data-dependent outputs**
- Messages = **System + User roles**
- Future = **Multimodal AI**

---