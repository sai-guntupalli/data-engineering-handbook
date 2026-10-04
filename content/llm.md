## [Main title](../README.md)
### [Interview questions](full.md)

# LLM and AI Terminology

Large language models are now part of the data platform, and data engineers are expected to speak the vocabulary: tokens, embeddings, RAG, fine-tuning, evals, and inference cost.

+ [What is a large language model?](#What-is-a-large-language-model)
+ [What is the difference between AI, ML, deep learning, and generative AI?](#What-is-the-difference-between-AI-ML-deep-learning-and-generative-AI)
+ [What are the key components of a transformer?](#What-are-the-key-components-of-a-transformer)
+ [What is attention and why does it matter?](#What-is-attention-and-why-does-it-matter)
+ [What are tokens and tokenization?](#What-are-tokens-and-tokenization)
+ [What is a context window?](#What-is-a-context-window)
+ [What are embeddings?](#What-are-embeddings)
+ [How do you measure similarity between embeddings?](#How-do-you-measure-similarity-between-embeddings)
+ [What is a vector database and when do you need one?](#What-is-a-vector-database-and-when-do-you-need-one)
+ [What is RAG and how does it work?](#What-is-RAG-and-how-does-it-work)
+ [How do you chunk documents for RAG?](#How-do-you-chunk-documents-for-RAG)
+ [What is prompt engineering?](#What-is-prompt-engineering)
+ [What are temperature, top-p, and top-k?](#What-are-temperature-top-p-and-top-k)
+ [What is the difference between parameters, weights, and hyperparameters?](#What-is-the-difference-between-parameters-weights-and-hyperparameters)
+ [What are pretraining, fine-tuning, instruction tuning, RLHF, and DPO?](#What-are-pretraining-fine-tuning-instruction-tuning-RLHF-and-DPO)
+ [What are LoRA, PEFT, and quantization?](#What-are-LoRA-PEFT-and-quantization)
+ [What is hallucination and how do you reduce it?](#What-is-hallucination-and-how-do-you-reduce-it)
+ [What is grounding and why do citations matter?](#What-is-grounding-and-why-do-citations-matter)
+ [What are evals and how do you evaluate an LLM application?](#What-are-evals-and-how-do-you-evaluate-an-LLM-application)
+ [What is LLM-as-a-judge?](#What-is-LLM-as-a-judge)
+ [What is an AI agent and what is tool calling?](#What-is-an-AI-agent-and-what-is-tool-calling)
+ [What is the Model Context Protocol (MCP)?](#What-is-the-Model-Context-Protocol-MCP)
+ [What are guardrails, prompt injection, and PII risks?](#What-are-guardrails-prompt-injection-and-PII-risks)
+ [What is the difference between training and inference?](#What-is-the-difference-between-training-and-inference)
+ [What are TTFT, tokens per second, KV cache, and batching?](#What-are-TTFT-tokens-per-second-KV-cache-and-batching)
+ [How do you observe and cost-manage an LLM application?](#How-do-you-observe-and-cost-manage-an-LLM-application)
+ [What is drift for LLM and AI systems?](#What-is-drift-for-LLM-and-AI-systems)
+ [What is the data engineer's role in an AI platform?](#What-is-the-data-engineers-role-in-an-AI-platform)
+ [What are common LLM and AI interview traps?](#What-are-common-LLM-and-AI-interview-traps)
+ [Real world use cases for LLMs in data engineering](#Real-world-use-cases-for-LLMs-in-data-engineering)

## What is a large language model?

A large language model (LLM) is a neural network trained to predict the next token in a sequence. Trained on enormous text corpora, it learns grammar, facts, and patterns that let it generate text, answer questions, summarize, translate, write code, and follow instructions. Chat models add instruction tuning and alignment so the raw next-token predictor behaves like an assistant.

Two properties matter for interviews:

+ **It is a statistical model, not a database.** It has no built-in truth; it produces the most plausible continuation. That is why retrieval, grounding, and evals exist.
+ **It is frozen at inference time** (unless you fine-tune). Updating knowledge means changing the prompt/context (RAG) or retraining/adapting the model.

[Table of Contents](#LLM-and-AI-Terminology)

## What is the difference between AI, ML, deep learning, and generative AI?

```text
AI                 machines performing tasks that need intelligence (broadest)
 └── ML            systems that learn patterns from data instead of explicit rules
      └── DL       ML using deep neural networks (many layers)
           └── GenAI   models that generate new content (text, images, audio, code)
                └── LLM  generative models over token sequences
```

+ **Classical ML**: logistic regression, gradient boosting, clustering - still the right answer for tabular prediction.
+ **Deep learning**: CNNs, RNNs, transformers.
+ **Generative AI**: diffusion models, LLMs, speech models.
+ **LLM**: a generative model whose input and output are tokens.

[Table of Contents](#LLM-and-AI-Terminology)

## What are the key components of a transformer?

The transformer is the architecture behind modern LLMs:

+ **Token embeddings** - each token becomes a vector.
+ **Positional encoding** - order information, since attention itself is order-agnostic.
+ **Self-attention layers** - every token attends to every other token in the context.
+ **Multi-head attention** - several attention "heads" learn different relationships (syntax, coreference, position).
+ **Feed-forward network** - per-token transformation, where much of the parameter count lives.
+ **Residual connections and layer norm** - stable deep training.
+ **Stacking** - many identical blocks; decoder-only stacks generate text left to right.

```text
input tokens -> embeddings + positions -> [attention -> FFN] x N -> next-token probabilities
```

[Table of Contents](#LLM-and-AI-Terminology)

## What is attention and why does it matter?

Attention lets each token weight every other token in the context: it computes query, key, and value projections and mixes values by softmax-normalized query-key similarity.

```text
Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V
```

Why it matters operationally: attention cost grows roughly with the **square of the context length**, which is why long contexts are expensive, why KV caching exists, and why retrieval (fetching only relevant chunks) is often cheaper than stuffing a huge prompt.

[Table of Contents](#LLM-and-AI-Terminology)

## What are tokens and tokenization?

A token is a subword unit produced by a tokenizer (commonly Byte-Pair Encoding). Models read and write tokens, and pricing, context limits, and latency are all measured in tokens - not characters or words.

```python
# Rough token counting with tiktoken (OpenAI-compatible encodings)
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
text = "Data engineering pipelines move data reliably."
ids = enc.encode(text)
print(len(ids), ids)
print(enc.decode(ids))
```

Rules of thumb for interviews: English averages roughly 4 characters per token (about 0.75 words); code, JSON, and non-Latin scripts tokenize less efficiently; whitespace and punctuation count.

[Table of Contents](#LLM-and-AI-Terminology)

## What is a context window?

The context window is the maximum number of tokens the model can attend to in one request - prompt plus generated output. Exceeding it means truncation, summarization, or retrieval.

```text
| system prompt | retrieved context | conversation history | user question | reserved output |
|<--------------------------- context window --------------------------->|
```

Practical implications:

+ Long conversations must be summarized or windowed, or they eventually fail.
+ More context is not always better: irrelevant tokens dilute attention and increase cost ("lost in the middle").
+ Chunk sizes and top-k in RAG are constrained by the context budget.

[Table of Contents](#LLM-and-AI-Terminology)

## What are embeddings?

An embedding is a dense vector that represents the meaning of text (or an image) in a high-dimensional space, produced by an embedding model. Texts with similar meaning land near each other.

```python
import numpy as np

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

# vectors come from an embedding model such as text-embedding-3-small or bge/e5
assert cosine(np.array([0.1, 0.9, 0.2]), np.array([0.12, 0.88, 0.25])) > 0.99
```

Key interview points: embeddings power semantic search, clustering, deduplication, recommendations, and classification. Changing the embedding model invalidates the whole index - you must re-embed the corpus.

[Table of Contents](#LLM-and-AI-Terminology)

## How do you measure similarity between embeddings?

+ **Cosine similarity** - angle between vectors, ignores magnitude; the default for text.
+ **Dot product** - equals cosine when vectors are normalized; common in fast indexes.
+ **Euclidean (L2) distance** - geometric distance; used by some libraries.

```python
import numpy as np

a = np.array([1.0, 0.0, 0.0])
b = np.array([0.9, 0.1, 0.0])
print("cosine:", float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))))
print("dot:", float(a @ b))
print("l2:", float(np.linalg.norm(a - b)))
```

Whatever metric you choose, it must match the one the index was built with; mixing metrics silently degrades retrieval quality.

[Table of Contents](#LLM-and-AI-Terminology)

## What is a vector database and when do you need one?

A vector database stores embeddings and supports fast approximate nearest-neighbor (ANN) search with metadata filters. Options span purpose-built systems (Pinecone, Weaviate, Qdrant, Milvus), libraries (FAISS, hnswlib), and features inside existing platforms (pgvector in Postgres, Elasticsearch/OpenSearch kNN, BigQuery vector search, Snowflake/Snowpark, Databricks Vector Search).

```sql
-- pgvector: create an index and search with a metadata filter
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE doc_chunks (
    chunk_id    bigserial PRIMARY KEY,
    doc_id      text NOT NULL,
    tenant_id   text NOT NULL,
    content     text NOT NULL,
    embedding   vector(1536) NOT NULL
);

CREATE INDEX ON doc_chunks USING hnsw (embedding vector_cosine_ops);

SELECT doc_id, content, 1 - (embedding <=> :query_embedding) AS score
FROM doc_chunks
WHERE tenant_id = :tenant
ORDER BY embedding <=> :query_embedding
LIMIT 8;
```

Do you need a dedicated vector database? Not always. If you already run Postgres or OpenSearch and the corpus is moderate, an extension or native kNN is simpler and keeps one platform to operate. Reach for a dedicated store when you need very large scale, high QPS, or advanced filtering and hybrid search.

[Table of Contents](#LLM-and-AI-Terminology)

## What is RAG and how does it work?

Retrieval-Augmented Generation means fetching relevant context at query time and putting it in the prompt so the model answers from your data instead of from memory.

```text
indexing:   documents -> chunk -> embed -> vector index (+ metadata)
query:      question -> embed -> top-k search -> rerank -> prompt with context -> LLM -> answer + citations
```

```python
def answer(question: str, tenant: str, k: int = 6) -> str:
    q_vec = embed(question)
    hits = vector_search(q_vec, tenant=tenant, k=k)          # list of {content, doc_id, score}
    ranked = rerank(question, hits)                            # optional cross-encoder reranker
    context = "\n\n".join(f"[{h['doc_id']}] {h['content']}" for h in ranked[:k])
    prompt = (
        "Answer only from the context. Cite document ids. "
        "If the context is insufficient, say so.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    return llm(prompt)
```

Why it dominates enterprise AI: you get freshness, tenant isolation, auditable sources, and no retraining. The hard parts are chunking, metadata filters, evaluation, and keeping the index fresh.

[Table of Contents](#LLM-and-AI-Terminology)

## How do you chunk documents for RAG?

Chunking is the highest-leverage RAG decision. Too large and you dilute the context; too small and you lose the meaning a question depends on.

Strategies:

+ **Fixed size with overlap** - simple, predictable token counts; overlap preserves sentence boundaries.
+ **Recursive splitting** - split on paragraph, then sentence, then characters.
+ **Structure-aware** - split by Markdown headings, HTML sections, or table rows.
+ **Semantic** - split where embedding similarity between adjacent sentences drops.

```python
def chunk_text(text: str, size: int = 800, overlap: int = 120) -> list[str]:
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        end = start + size
        chunks.append(" ".join(words[start:end]))
        if end >= len(words):
            break
        start = end - overlap
    return chunks

# always attach metadata: it is what makes filters and citations possible
chunks = [{"text": c, "doc_id": "policy-v3", "section": "retention", "updated_at": "2026-09-30"}
          for c in chunk_text(open("policy.md").read())]
```

Attach metadata (document id, version, tenant, effective date, section) and store it next to the vector so you can filter, cite, and expire.

[Table of Contents](#LLM-and-AI-Terminology)

## What is prompt engineering?

Prompt engineering is designing the instructions and context so a model reliably produces the output you need.

Patterns worth naming:

+ **Zero-shot** - instruction only.
+ **Few-shot** - a handful of input/output examples that demonstrate the format.
+ **Chain-of-thought** - ask for intermediate reasoning before the answer (use with care when exposing reasoning).
+ **Structured output** - require JSON matching a schema so downstream code can parse it.
+ **Role/system prompt** - durable behaviour, tone, and constraints.

```python
prompt = """You are a data quality assistant.
Return JSON only: {"severity": "low|medium|high", "reason": "..."}.

Rules:
- severity is high if the partition is empty or schema changed.
- severity is medium if null rate > 5%.
- severity is low otherwise.

Input: null_rate=0.08, empty_partition=false, schema_changed=false
Output:"""
```

Treat prompts as versioned code: store them in Git, review changes, and test them with evals.

[Table of Contents](#LLM-and-AI-Terminology)

## What are temperature, top-p, and top-k?

These parameters control sampling randomness at generation time:

| Parameter | What it does | Typical use |
|---|---|---|
| `temperature` | scales logits; 0 = deterministic, higher = more random | 0-0.3 for extraction/SQL, 0.7+ for brainstorming |
| `top_p` (nucleus) | sample from the smallest set of tokens whose probability sums to p | 0.9-0.95 general use |
| `top_k` | sample from the k highest-probability tokens | library-dependent; alternative to top_p |
| `max_tokens` | cap on generated tokens | cost and latency control |
| `stop` | sequences that end generation | structured formats, delimiters |

```python
response = llm.chat(
    messages=[{"role": "user", "content": "Write a SQL CASE expression for order status."}],
    temperature=0.0,      # deterministic: we want correct syntax, not creativity
    top_p=1.0,
    max_tokens=256,
)
```

Interview point: for pipelines that parse model output, prefer temperature 0 plus schema validation, not "please be accurate".

[Table of Contents](#LLM-and-AI-Terminology)

## What is the difference between parameters, weights, and hyperparameters?

+ **Weights/parameters** - the learned numbers inside the network (billions for large models). "7B model" means ~7 billion parameters.
+ **Hyperparameters** - choices set before training: learning rate, batch size, layers, heads, context length, LoRA rank.
+ **Inference parameters** - runtime knobs: temperature, top-p, max tokens.

```text
model size (7B/70B/405B) drives VRAM, latency, and cost:
  fp16 ~= 2 bytes/parameter -> ~14 GB for 7B, ~140 GB for 70B
  int8 ~= 1 byte/parameter, int4 ~= 0.5 byte/parameter (quantization)
```

[Table of Contents](#LLM-and-AI-Terminology)

## What are pretraining, fine-tuning, instruction tuning, RLHF, and DPO?

```text
pretraining        next-token prediction on a huge corpus          -> base model
instruction tuning supervised examples of instructions + answers   -> follows commands
RLHF               reward model + reinforcement learning           -> aligns to human preference
DPO                direct preference optimization on chosen/rejected pairs (simpler than RLHF)
fine-tuning        further training on your domain data            -> adapts style/format/domain
```

Decision guide:

+ Need **fresh, private, citable facts** -> RAG, not fine-tuning.
+ Need **consistent format, tone, or domain jargon** -> fine-tuning or few-shot prompting.
+ Need **predictable structured extraction** -> prompt + schema validation first, fine-tune only if quality plateaus.

[Table of Contents](#LLM-and-AI-Terminology)

## What are LoRA, PEFT, and quantization?

+ **PEFT** - parameter-efficient fine-tuning: train a small number of extra parameters instead of all weights.
+ **LoRA** - low-rank adapters inserted into attention layers; the base model stays frozen, adapters are small files you can swap.
+ **QLoRA** - LoRA on a 4-bit quantized base model, which makes fine-tuning large models feasible on modest GPUs.
+ **Quantization** - reduce weight precision (int8/int4, GPTQ, AWQ, GGUF) to cut memory and cost, at some quality risk.

```text
full fine-tune 70B : many GPUs, large checkpoints
LoRA 70B           : one/few GPUs, adapters of tens of MB
int4 served model  : fits smaller GPUs, lower cost, validate quality with evals
```

[Table of Contents](#LLM-and-AI-Terminology)

## What is hallucination and how do you reduce it?

Hallucination is fluent output that is not supported by facts. It is a property of a probabilistic model, not a bug you can fully remove.

Mitigations that work in production:

+ **Ground with retrieval** and instruct the model to answer only from context.
+ **Require citations** and verify that cited ids exist and contain the claim.
+ **Constrain output** with JSON schemas or grammars, then validate.
+ **Lower temperature** for extraction tasks.
+ **Add a refusal path** ("say I do not know") and test it in evals.
+ **Human review** for high-stakes actions, plus logging for audit.

```python
import json

def safe_extract(raw: str) -> dict:
    data = json.loads(raw)                     # fail loudly instead of parsing garbage
    if data.get("severity") not in {"low", "medium", "high"}:
        raise ValueError("invalid severity")
    return data
```

[Table of Contents](#LLM-and-AI-Terminology)

## What is grounding and why do citations matter?

Grounding means tying the model's answer to a verifiable source: retrieved passages, query results, or tool outputs. Citations make that verifiable for a user or an auditor.

For a data platform, grounding is usually: retrieve from a governed table/vector index, include stable identifiers, and store the prompt, context ids, model version, and output for every call. If a number appears in an answer, the pipeline should be able to show which rows produced it.

[Table of Contents](#LLM-and-AI-Terminology)

## What are evals and how do you evaluate an LLM application?

Evals are the test suite for an AI feature. They combine deterministic checks, model-graded scores, and human review.

```text
offline evals
  +-- dataset of inputs with expected outputs or rubrics
  +-- deterministic checks: JSON schema valid, SQL executes, citation ids exist
  +-- semantic metrics: exact match, F1, retrieval recall@k, answer faithfulness
  +-- model-graded: LLM-as-a-judge with a rubric
  +-- regression suite: run on every prompt/model change

online signals
  +-- user feedback (thumbs, edits), task success, escalation rate
  +-- latency, token cost, error rate, refusal rate
```

```python
def run_eval(cases, app):
    results = []
    for case in cases:
        out = app(case["input"])
        results.append({
            "id": case["id"],
            "schema_ok": validate_schema(out),
            "retrieval_hit": case["expected_doc"] in out.get("cited_docs", []),
            "answer_ok": judge(case["input"], out["answer"], rubric=case["rubric"]),
        })
    pass_rate = sum(all(r[k] for k in ("schema_ok", "retrieval_hit", "answer_ok")) for r in results) / len(results)
    return {"n": len(results), "pass_rate": pass_rate, "results": results}
```

Interview point: you cannot improve what you cannot measure - define the eval set before tuning prompts.

[Table of Contents](#LLM-and-AI-Terminology)

## What is LLM-as-a-judge?

Using a strong model to score another model's output against a rubric. It scales human-style judgement cheaply, but has known biases: position bias, verbosity bias, self-preference.

Rules for using it responsibly: provide clear rubrics and reference answers, randomize order, calibrate against a human-labelled sample, and keep deterministic checks where they are possible (valid JSON, executing SQL, citation existence).

[Table of Contents](#LLM-and-AI-Terminology)

## What is an AI agent and what is tool calling?

A **tool/function call** lets the model request a structured action (search, SQL query, API call) instead of only emitting text. The application executes the tool and returns the result to the model.

An **agent** is a loop: plan -> call tools -> observe -> decide -> repeat until done. Add memory, guardrails, and a step/budget limit.

```python
tools = [{
    "type": "function",
    "function": {
        "name": "run_sql",
        "description": "Run a read-only SQL query against the analytics warehouse",
        "parameters": {
            "type": "object",
            "properties": {"sql": {"type": "string"}},
            "required": ["sql"],
        },
    },
}]

# the model returns a tool call; your code validates and executes it
decision = llm.chat(messages, tools=tools, tool_choice="auto")
if decision.tool_call == "run_sql":
    rows = warehouse.query(validate_read_only(decision.arguments["sql"]))
```

Data-engineering relevance: every agent action is a security boundary. Enforce read-only credentials, allow-listed tools, row limits, timeouts, and audit logging.

[Table of Contents](#LLM-and-AI-Terminology)

## What is the Model Context Protocol (MCP)?

MCP is an open protocol for connecting AI applications to external tools and data sources through standardized servers. Instead of every IDE or agent shipping a custom integration per system, an MCP server exposes resources, tools, and prompts that any compatible client can call.

For data teams the practical value is reuse: one governed MCP server for the warehouse, catalog, and ticketing system, consumed by multiple assistants. The risks are the same as any tool integration - authorization, prompt injection through retrieved content, and auditability - so servers should run with least-privilege credentials and log every call.

[Table of Contents](#LLM-and-AI-Terminology)

## What are guardrails, prompt injection, and PII risks?

+ **Direct prompt injection** - a user asks the model to ignore its instructions.
+ **Indirect prompt injection** - malicious text inside retrieved documents or web pages instructs the model; this is the dangerous one for RAG.
+ **Data exfiltration** - the model is tricked into revealing system prompts, other tenants' data, or secrets.
+ **PII exposure** - personal data flows into prompts, logs, or third-party model providers.

Controls that matter:

```text
input:   redact PII, detect injection patterns, enforce tenant filters on retrieval
context: treat retrieved text as untrusted data, never as instructions
tools:   read-only by default, allow-lists, row limits, no direct DDL/DML
output:  schema validation, PII scanning, citation checks
ops:     per-tenant logging, retention limits, provider data-processing agreements, no-training flags
```

[Table of Contents](#LLM-and-AI-Terminology)

## What is the difference between training and inference?

+ **Training** - learning weights from data: expensive, batch, GPU-heavy, done rarely.
+ **Inference** - using the trained model: latency-sensitive, cost per token, done constantly.

```text
training   : GPU-days to GPU-months, data pipelines, checkpoints, repeatable experiments
inference  : milliseconds to seconds per request, autoscaling, caching, cost per 1M tokens
```

Modern data platforms support both: training needs curated, versioned datasets and feature tables; inference needs low-latency access to features and retrieval.

[Table of Contents](#LLM-and-AI-Terminology)

## What are TTFT, tokens per second, KV cache, and batching?

+ **TTFT (time to first token)** - latency until streaming starts; dominated by prompt processing (prefill).
+ **Inter-token latency / throughput** - tokens per second while generating; dominated by decoding.
+ **KV cache** - cached key/value tensors for previous tokens, so generation does not recompute the whole context.
+ **Continuous batching** - serving many requests in one batch to raise GPU utilization; a key reason inference servers such as vLLM or TGI beat naive per-request serving.

```text
prompt tokens  -> prefill (compute-bound, sets TTFT)
output tokens  -> decode (memory-bandwidth-bound, sets tokens/sec)
cost           ~= input_tokens * input_price + output_tokens * output_price
```

[Table of Contents](#LLM-and-AI-Terminology)

## How do you observe and cost-manage an LLM application?

```python
import time

def traced_llm_call(prompt: str, model: str) -> str:
    started = time.perf_counter()
    resp = client.chat(model=model, messages=[{"role": "user", "content": prompt}])
    latency_ms = (time.perf_counter() - started) * 1000
    log_event({
        "event": "llm_call",
        "model": model,
        "prompt_tokens": resp.usage.prompt_tokens,
        "completion_tokens": resp.usage.completion_tokens,
        "latency_ms": latency_ms,
        "cost_usd": estimate_cost(model, resp.usage),
        "prompt_version": "dq-explainer-v3",
        "trace_id": current_trace_id(),
    })
    return resp.text
```

What to track: token usage and cost per feature/tenant, latency percentiles (TTFT and total), error and refusal rates, retrieval hit rate, prompt/model/prompt-version, and eval pass rate over time. Cache identical or semantically similar requests, route easy traffic to smaller models, cap output tokens, and summarize conversation history.

[Table of Contents](#LLM-and-AI-Terminology)

## What is drift for LLM and AI systems?

Drift is change over time that degrades quality:

+ **Data drift** - input distribution changes (new products, new languages, new tenants).
+ **Concept drift** - the relationship between input and correct output changes (fraud patterns, policy changes).
+ **Embedding/index drift** - source documents change but the vector index is stale.
+ **Model drift** - the provider updates the model behind the same name.

Detection: monitor input distributions and retrieval scores, track eval pass rate on a fixed golden set, alert on changes in refusal rate or answer length, and re-run evals after any model or prompt change.

[Table of Contents](#LLM-and-AI-Terminology)

## What is the data engineer's role in an AI platform?

+ **Build the retrieval corpus**: ingest documents/tables, chunk, embed, keep the index fresh (CDC or scheduled rebuilds), and expire deleted content.
+ **Serve features and context with low latency**: feature tables for training, online stores for inference, vector search for RAG.
+ **Govern data**: PII redaction, tenant isolation, lineage from source to prompt, retention policies, access control.
+ **Instrument and cost-control**: token/cost metrics, prompt and model versioning, evals in CI, caching.
+ **Keep pipelines reproducible**: dataset versions, deterministic transforms, and tests for the data that feeds models.

The interview framing: LLMs did not replace data engineering - they added a new consumer of governed, well-modeled, low-latency data.

[Table of Contents](#LLM-and-AI-Terminology)

## What are common LLM and AI interview traps?

+ Saying "fine-tuning" when the real need is fresh data - that is RAG.
+ Treating the context window as unlimited, then wondering why answers degrade.
+ Skipping evals and judging quality by vibes.
+ Ignoring retrieval quality while tuning the prompt.
+ Confusing tokens with words when estimating cost.
+ Trusting model output as structured data without schema validation.
+ Letting retrieved content act as instructions (indirect prompt injection).
+ Forgetting to re-embed when the embedding model or chunking strategy changes.
+ Assuming the model behind an API name never changes; pin versions and re-run evals.

[Table of Contents](#LLM-and-AI-Terminology)

## Real world use cases for LLMs in data engineering

### 1. RAG over a governed lakehouse

Documents and tables are ingested from S3/SharePoint, chunked with metadata, embedded, and indexed in pgvector or OpenSearch. A support assistant answers with citations, filtered per tenant.

```python
hits = vector_search(embed(question), tenant=tenant, k=8, filters={"effective_to": None})
answer = llm(build_prompt(question, hits))
assert all(c in known_doc_ids for c in answer.cited_docs)
```

Why it fits: the data platform already owns ingestion, governance, and freshness; RAG turns those into grounded answers.

### 2. Keeping a vector index fresh with CDC

When a source row changes, the pipeline re-chunks and re-embeds only that document, then upserts into the index and deletes stale chunk ids.

```text
CDC event -> re-chunk document -> embed -> upsert chunks -> delete removed chunk ids
```

Why it fits: staleness is the most common RAG failure; CDC keeps retrieval as current as the warehouse.

### 3. Document processing and extraction pipelines

Invoices, contracts, and forms are parsed (OCR where needed), split into sections, and passed through structured extraction with schema validation, then loaded into warehouse tables for analysis.

```python
for doc in documents:
    raw = llm(extract_prompt(doc.text))
    record = safe_extract(raw)          # JSON schema + business rules
    warehouse.insert("finance.invoices", record)
```

Why it fits: it converts unstructured documents into governed tables that analysts and auditors can query.

### 4. Text-to-SQL with a semantic layer

Business users ask questions in natural language; the system retrieves table/column descriptions from the catalog, generates SQL against a curated semantic model, validates it as read-only, executes it, and explains the result.

```text
question -> catalog retrieval -> SQL generation -> read-only validation -> execute -> explain
```

Why it fits: the semantic layer constrains the model, which is far more reliable than letting it invent tables.

### 5. Embeddings as features for search and recommendations

Product and content embeddings are computed nightly, stored as features, and used for semantic search, similar-item recommendations, and deduplication.

```python
embeddings = embed_batch(catalog_texts)
write_feature_table("ml.item_embeddings", embeddings, keys=item_ids)
```

Why it fits: embedding tables are just another versioned feature pipeline with freshness and drift monitoring.

### 6. Cost and governance program for AI features

The platform team tracks tokens, cost, latency, and eval pass rate per feature; routes simple requests to smaller models; caches repeated queries; and keeps PII out of prompts with redaction plus provider no-training settings.

Why it fits: without this, an AI feature becomes an unowned, unbounded bill and a compliance risk.

[Table of Contents](#LLM-and-AI-Terminology)
