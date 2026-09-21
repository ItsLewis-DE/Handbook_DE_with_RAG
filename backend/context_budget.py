import json
import os
from functools import lru_cache

from transformers import AutoTokenizer

NUM_CTX = 8192 #context window tối đa
NUM_PREDICT = 768 #output token
TEMPLATE_MARGIN = 512 #token đề phòng vượt quá


def render_context(passages):
    return "\n\n".join(
        f"[S{index}]\n{doc.page_content}"
        for index, doc in enumerate(passages, 1)
    )


class TokenBudget:
    def __init__(self, tokenizer, prompt_factory, schema):
        self.tokenizer = tokenizer
        self.prompt_factory = prompt_factory
        self.schema_tokens = len(tokenizer.encode(
            json.dumps(schema, ensure_ascii=False), add_special_tokens=False,
        ))

    def input_tokens(self, question, passages, feedback="Không có."):
        prompt = self.prompt_factory().invoke({
            "question": question, "context": render_context(passages),
            "feedback": feedback,
        })
        roles = {"human": "user", "ai": "assistant", "system": "system"}
        messages = [
            {"role": roles[m.type], "content": m.content}
            for m in prompt.to_messages()
        ]
        return len(self.tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True,
            enable_thinking=False,
        ))

    def fits(self, question, passages, feedback="Không có."):
        return (
            self.input_tokens(question, passages, feedback)
            + self.schema_tokens + TEMPLATE_MARGIN + NUM_PREDICT <= NUM_CTX
        )

    def pack(self, question, passages):
        selected = []
        for passage in passages:
            if self.fits(question, selected + [passage]):
                selected.append(passage)
        return selected


@lru_cache(maxsize=1)
def get_budget():
    from answering import AnswerResult, build_prompt

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
    return TokenBudget(tokenizer, build_prompt, AnswerResult.model_json_schema())