from llama_index.core.prompts import PromptTemplate
from llama_index.core.response_synthesizers import get_response_synthesizer


def get_strict_prompt():
    return PromptTemplate(
        """
You MUST answer using ONLY the provided context.

Rules:
- Do NOT use prior knowledge
- Do NOT guess
- If answer not present, respond EXACTLY:
  Not found in knowledge base.

Instructions:
- Provide a detailed, comprehensive answer
- Cover all relevant points from the context
- Do not shorten or summarize excessively
- Expand explanations clearly

Context:
{context_str}

Question:
{query_str}

Answer:
"""
    )



def get_synthesizer(llm):
    prompt = get_strict_prompt()

    return get_response_synthesizer(
        text_qa_template=prompt,
        response_mode="tree_summarize",
        llm=llm,
        streaming=True
    )
