"""A dependency-free client for any OpenAI-compatible chat endpoint.

Works with vLLM (`vllm serve <model>` exposes /v1/chat/completions), SGLang,
llama.cpp server, Ollama's OpenAI endpoint, and hosted APIs that speak the same
protocol. It returns a plain `prompt -> text` callable, which is the interface
every ragkit component expects (AgenticRAG, T2RAG, ...).

    from ragkit.llm import OpenAICompatibleLLM
    llm = OpenAICompatibleLLM("http://localhost:8000/v1", model="Qwen/Qwen2.5-7B-Instruct",
                              stop=["</search>", "</answer>"], append_stop=True)
    AgenticRAG(llm, retriever.retrieve_text).run("Who directed Move (1970)?")

`append_stop=True` re-appends the stop string the server matched (servers strip
it), so ragkit.agentic.parse_action still sees a closed tag.
"""

import json
import os
import urllib.request
from typing import List, Optional


class OpenAICompatibleLLM:
    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None,
                 temperature: float = 0.0, max_tokens: int = 512, stop: Optional[List[str]] = None,
                 append_stop: bool = False, system: Optional[str] = None, timeout: float = 120.0):
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "EMPTY")
        self.temperature, self.max_tokens, self.stop = temperature, max_tokens, stop
        self.append_stop, self.system, self.timeout = append_stop, system, timeout

    def _payload(self, prompt: str) -> dict:
        messages = ([{"role": "system", "content": self.system}] if self.system else [])
        messages.append({"role": "user", "content": prompt})
        body = {"model": self.model, "messages": messages,
                "temperature": self.temperature, "max_tokens": self.max_tokens}
        if self.stop:
            body["stop"] = self.stop
        return body

    def __call__(self, prompt: str) -> str:
        req = urllib.request.Request(
            self.url, data=json.dumps(self._payload(prompt)).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            data = json.load(r)
        choice = data["choices"][0]
        text = choice["message"]["content"] or ""
        if self.append_stop and self.stop and choice.get("finish_reason") == "stop":
            # Servers strip the matched stop string; restore the one whose opening tag is unclosed.
            for s in self.stop:
                opener = s.replace("</", "<")
                if opener in text and s not in text:
                    text += s
                    break
        return text
