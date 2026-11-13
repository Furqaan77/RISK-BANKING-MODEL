"""LLM port (AD-6, AD-19). The LLM may only REPHRASE an evidence-backed answer; it never decides, never sees raw
customer data, never changes anything. Default = NullLLM (template text returned unchanged).

To add later: an adapter for the bank's approved model or a local model (e.g. vLLM). Guardrail: every number in the
rephrased text must appear in the facts; otherwise the template answer is used.
"""
import re


class NullLLM:
    name = "none (template only)"

    def rephrase(self, template_answer: str, facts: dict) -> str:
        return template_answer


def guarded(llm, template_answer: str, facts: dict) -> str:
    text = llm.rephrase(template_answer, facts)
    nums_out = set(re.findall(r"\d[\d,]*\.?\d*", text))
    nums_in = set(re.findall(r"\d[\d,]*\.?\d*", template_answer))
    return text if nums_out <= nums_in else template_answer
