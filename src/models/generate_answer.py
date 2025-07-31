from llama_cpp import Llama


def generate_answer(message: str, data: list[dict]) -> str:
    if data:
        context = "\n\n".join([r["entity"]["chunks"] for r in data])
        prompt = f"""Contexto:\n{context}\n\nPergunta: {message}\nResposta:"""
    else:
        prompt = f"""Pergunta: {message}\nResposta:"""

    llm = Llama(model_path="llama-3.2-3b-instruct-q4_k_m.gguf", n_threads=4, n_ctx=4096)

    answer = llm.create_completion(
        prompt=prompt, max_tokens=None, temperature=0.7, top_p=0.9
    )

    return answer["choices"][0]["text"].strip()
