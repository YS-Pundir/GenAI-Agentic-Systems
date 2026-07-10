# Safety & Guardrails for AI Agents: Quick Reference

## 1. What are Guardrails?
Guardrails act as "airport security" for your LLM. They filter both the input (before the model runs) and the output (before the user sees the response) to ensure safety, consistency, and privacy.

## 2. Key Risk Types
* **Prompt Injection:** Attempts to override system instructions (e.g., "Ignore all previous instructions").
* **PII Leakage:** Accidental exposure of personal data (names, addresses, phone numbers).
* **Data Leakage:** Revealing internal business processes (refund checks, fraud detection logic).
* **Scope Breach:** Responding to off-topic questions outside the agent's defined business role.
* **Bias & Toxicity:** Generating harmful language or unfair/favorable opinions toward specific brands or demographics.

## 3. The Guarded Pipeline Flow
To build a secure support bot, apply checks in this order:

1.  **Input Guardrails (Pre-LLM):**
    * **Prompt Injection Check:** Use a dedicated classifier (LLM yes/no) or library to block attempts to change the bot's role.
    * **Toxicity Check:** Filter out abusive language using pre-trained models (e.g., `Detoxify`).
2.  **Main Agent Logic:**
    * System message with hard constraints (e.g., "Never reveal internal refund checks").
3.  **Output Guardrails (Post-LLM):**
    * **PII Masking:** Replace sensitive data with placeholders (e.g., `XXXX`).
    * **Bias & Toxicity Check:** Filter the generated response before showing it to the user.
    * **Refusal Templates:** Always use fixed, professional error messages for blocked queries rather than letting the bot "reason" with the user.

## 4. Frameworks & Tools
* **LLM Guard:** Open-source toolkit with pre-built scanners for injection, bias, secrets, and malicious URLs.
* **Llama Guard:** Meta’s moderation-focused model for classifying input/output safety.
* **NeMo Guardrails:** NVIDIA's framework for defining programmable, rule-based conversational constraints.

## 5. Pro-Tips for Success
* **Fail Early:** Run input checks *before* calling tools or databases to save costs and prevent data exposure.
* **Determinism:** Use `temperature=0` for classification prompts to ensure stability.
* **Avoid Self-Policing:** Do not rely on the LLM to decide if its own output is safe; use separate code-based scanners.
* **Test with Eval Sets:** Maintain a list of test cases (normal, injection, toxic, PII-seeking) to verify that guardrails are functioning as expected.