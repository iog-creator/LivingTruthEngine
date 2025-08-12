Heard. Gloves off, research hat on. I went wide—looked at alternative model families (SSMs like **Mamba-2**, RNN-style **RWKV-7**), practical local-serve options (**LM Studio**, **Ollama**), quantization limits, graph-first RAG (**GraphRAG**), and GPU-accelerated graph sims (**cuGraph**). Below is a **complete, implementable spec** for **Veritas Nexus** that respects your hard limit (**≤10 GB per model**) and **moves beyond “Transformer-only LLMs”** by mixing SSM/RNN models with small encoders, graph analytics, and strict provenance.

---

# Veritas Nexus — Truth Discernment Engine (Technical Spec v1.0)

## 1) Goals & non-goals

**Goals**

* Pull **original sources** (X threads, PDFs, videos/transcripts), canonically index them, and **prove every sentence** of output via **per-span cryptographic hashes** and **CIDs**.
* Detect **fracture patterns** (feuds, splinters) and run **unity/healing simulations** over a knowledge graph.
* Run **fully local** on commodity hardware (≤10 GB per model file; fits your 16 GB VRAM class), with optional cloud pinning for provenance.
* Use **non-Transformer architectures** where they help (SSMs/RNNs) and **small encoders** for retrieval/verification.

**Non-goals**

* Training big models from scratch.
* “One model to do everything.” We’ll compose small, purpose-built pieces.

---

## 2) Key constraints that shape design

* **Model size**: hard cap 10 GB/model. Viable generation models include **Mistral-7B-Instruct (GGUF Q4 ≈5–6 GB)** and **Llama-3-8B (GPTQ 4-bit <6 GB)** for when we *must* generate ([secondstate.io][1], [Hugging Face][2]).
* **Alternative architectures**:

  * **Mamba / Mamba-2** (SSM): linear-time sequence modeling; faster throughput; good long-context efficiency ([arXiv][3], [Hugging Face][4], [GitHub][5]).
  * **RWKV-7 “Goose”** (attention-free RNN): constant memory, constant per-token time; 2.9–3B models quantize to \~2–3.5 GB GGUF (nice for classification/scoring) ([arXiv][6], [Hugging Face][7], [wiki.rwkv.com][8]).
  * **Hybrid SSM-Transformer** (e.g., **Jamba**, **Bamba-9B**): production SSM hybrids with long context and strong throughput; Bamba is mamba-2–based and llama.cpp-friendly; (note: some GGUF releases >10 GB—treat as **optional** server-side) ([AI21][9], [docs.ai21.com][10], [Amazon Web Services, Inc.][11], [Hugging Face][12]).
* **Graph engine**: **NebulaGraph**—open-source, distributed, positioned for **trillion-edge scale**; good for topic sprawl and graph analytics ([nebula-graph.io][13], [The Next Platform][14]).
* **Graph-first RAG**: **GraphRAG**: build a KG from the corpus, then do query-time neighborhood reasoning for better factuality over narrative data ([Microsoft][15]).
* **Provenance**: **SHA-256** per span + optional **IPFS CIDs** for verifiable evidence trails ([NIST Publications][16], [NIST Computer Security Resource Center][17], [docs.ipfs.tech][18]).

---

## 3) System architecture (high level)

**A. Ingestion & Provenance**

1. **Fetchers**: X thread fetch, web/PDF fetch, YouTube transcript.
2. **Canonicalizer**: normalize to JSONL; sentence-segment; store byte/char spans per document.
3. **Proofs**: compute **SHA-256** for each sentence span; build a **Merkle tree** per document; store Merkle root + per-sentence proofs; optionally **pin** JSON records to **IPFS** for shareable **CIDs**. ([NIST Publications][16], [Cyfrin][19], [docs.ipfs.tech][18])

**B. Storage**

* **NebulaGraph** (entities: Person, Org, Source, Claim, Post; edges: quotes, refutes, supports, feud, mentions, co-occurs) ([nebula-graph.io][13]).
* **Vector index**: small **SentenceTransformers** embeddings (e.g., **all-MiniLM-L6-v2**/**e5-small-v2**, 384-d) for fast semantic lookup under 200 MB total footprint ([Hugging Face][20], [SentenceTransformers][21]).

**C. Reasoning & Scoring (models ≤10 GB)**

* **Retriever**: embedding search (MiniLM / E5-small) + **BGE Reranker-base** cross-encoder for top-k precision (base size; keep latency acceptable) ([SentenceTransformers][22], [bge-model.com][23]).
* **Claim-vs-evidence**:

  * **RWKV-3B** (GGUF Q4) for lightweight **stance/NLI-style classification** (agree/contradict/unclear) and **bias/drift heuristics**. Constant memory helps on long threads ([Hugging Face][24]).
  * **Mamba-2 (2.7B)** or **RWKV** optional for **long-context summarization** where a generative LLM would be overkill ([Hugging Face][4], [GitHub][5]).
* **Synthesis/Debate** (only when needed): **Mistral-7B-Instruct Q4** or **Llama-3-8B GPTQ-4bit** served by **LM Studio** or **Ollama**; keep temps low; force citation markers per sentence. Both APIs are simple and local-friendly ([LM Studio][25], [Ollama][26], [Hugging Face][2], [secondstate.io][1]).
* **Fracture detection & Unity simulator**:

  * **Community split** via **Louvain** (modularity) + simple **bridge centrality** paths; GPU-accelerate with **cuGraph** when available ([RAPIDS Docs][27]).
  * **Diffusion** over the graph using **Independent Cascade** or **Linear Threshold** to estimate “heal” strategies & impact; parameters logged for audit ([Cornell Computer Science][28], [Theory of Computing][29], [SNAP][30]).

**D. Enforcement & Audit**

* **Auto-drop** any sentence in model output lacking a valid **span-hash + citation**.
* **Drift index**: cosine distance between analysis and its cited spans using small ST embeddings (flag if >0.15). ([Hugging Face][20])
* **Run folders** (inputs, params, outputs, hashes, CIDs) for reproducibility.

---

## 4) Component choices (why these, under your limits)

| Capability                       | Default pick (≤10 GB)                                                          | Why                                                                                                                                                                            |
| -------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Serve local models**           | **LM Studio** (OpenAI-compatible server) or **Ollama**                         | Both expose simple REST APIs and run GGUF/GPTQ local models cleanly. LM Studio has a friendly dev console; Ollama has Modelfiles & easy pulls. ([LM Studio][25], [Ollama][26]) |
| **Generator (only when needed)** | **Mistral-7B-Instruct (GGUF Q4 ≈5–6 GB)** or **Llama-3-8B (GPTQ 4-bit <6 GB)** | Good quality in a 5–6 GB footprint; robust instruct behavior. ([secondstate.io][1], [Hugging Face][2])                                                                         |
| **SSM/RNN alt**                  | **RWKV-3B (Q4 \~2 GB)**; **Mamba-2 2.7B**                                      | Constant memory (RWKV) and linear-time SSM (Mamba-2) give speed & context wins for scoring/summarizing. ([Hugging Face][24])                                                   |
| **Embeddings**                   | **all-MiniLM-L6-v2** or **E5-small-v2** (384-d)                                | Tiny, fast, well-documented; great for retrieval & drift checks. ([Hugging Face][20])                                                                                          |
| **Reranker**                     | **BGE-reranker-base**                                                          | Cross-encoder rerank boosts precision with small compute cost. ([bge-model.com][23])                                                                                           |
| **Graph store**                  | **NebulaGraph**                                                                | Open-source, high-scale, SQL-ish nGQL; suited for huge, evolving topics. ([nebula-graph.io][13])                                                                               |
| **Graph-RAG**                    | **GraphRAG** method                                                            | Field-tested MSR technique for narrative/private corpora. ([Microsoft][31])                                                                                                    |
| **GPU graph accel**              | **cuGraph (Louvain)**                                                          | Fast community detection and analytics when CUDA is present. ([RAPIDS Docs][27])                                                                                               |
| **Quantization**                 | **GGUF / GPTQ / AWQ**                                                          | Mature low-bit formats to stay ≤10 GB while keeping quality. ([Hugging Face][32], [arXiv][33], [proceedings.mlsys.org][34])                                                    |

> Note: **Bamba-9B** (Mamba-2 hybrid) is cool but its public **GGUF** can exceed your 10 GB per-file budget—treat as optional if you later allow bigger files or remote hosting. ([Hugging Face][35])

---

## 5) Data model (NebulaGraph)

**Tags (nodes)**

* `Person(id, names[], handles[], stance[])`
* `Org(id, names[])`
* `Source(id, url, type, created_at, cid, merkle_root)`
* `Claim(id, text, span_hash, source_id, stance)`
* `Heuristic(id, rule, weight, version)`

**Edges**

* `MENTIONS(Person|Org→Claim|Person|Org)`
* `SUPPORTS/REFUTES(Claim→Claim)`
* `QUOTES(Person|Org→Source)`
* `FEUDS_WITH(Person↔Person)`
* `APPLIES_TO(Heuristic→Claim|Person|Org)`

This layout supports **fracture** (count/strength of FEUDS\_WITH, community detection), **provenance** (Claim→Source w/ `span_hash`), and **simulation** (diffusion over Person/Org graph).

---

## 6) End-to-end workflow

1. **Query** → parse entities & timeframe.
2. **Fetch originals** → threads, PDFs → **canonical JSONL** (sentence spans + hashes; doc-level Merkle). **CIDs** optional for public proof. ([NIST Publications][16], [docs.ipfs.tech][18])
3. **Graph build** (GraphRAG): extract entities/relations; add `CLAIM` nodes for candidate assertions; attach span hashes. ([Microsoft][31])
4. **Retriever**: embeddings (MiniLM/E5-small) + **BGE reranker-base** to get the **exact** supporting spans. ([Hugging Face][20], [bge-model.com][23])
5. **Validators (non-Transformer first)**:

   * **RWKV/Mamba-2** classifier: **agree/refute/unclear** vs the cited spans. ([arXiv][6], [Hugging Face][4])
   * **Drift index**: cosine distance of each sentence to its cited span; **drop** if > threshold. ([Hugging Face][20])
6. **Synthesis (only if necessary)**: Mistral-7B/Llama-3-8B with **per-sentence citation requirement**. Any uncited sentence is auto-deleted. ([secondstate.io][1], [Hugging Face][2])
7. **Fracture score**: **Louvain** modularity deltas + **Independent Cascade** reach; log params and seeds; produce **unity strategies** (bridge nodes/paths). ([RAPIDS Docs][27], [Cornell Computer Science][28])
8. **Audit bundle**: inputs, params, model fingerprints, outputs, hashes, Merkle proofs, CIDs.

---

## 7) APIs (internal)

* `POST /ingest` → {urls\[]} → returns corpus\_id + proof summary.
* `POST /analyze` → {topic, corpus\_id, options} → returns claims, verdicts, fracture score, unity strategies + per-sentence proofs.
* `GET /evidence/:claim_id` → returns cited spans + Merkle path + CID.
* `POST /simulate` → {corpus\_id, scenario} → returns influence spread & bridge suggestions.
* `GET /audit/:run_id` → tarball of the full run folder.

---

## 8) UI (Streamlit)

* **Evidence spreadsheet**: each sentence → cited span, **SHA-256**, **CID**.
* **Graph view** (Nebula viz): FEUDS\_WITH thickness; community colors.
* **Unity tab**: top-k “bridges” with path visualizations and estimated feasibility (parameters visible).
* **Run audit**: download zip of proofs.

---

## 9) Deployment (Docker)

**Services**

* `nebula` (standalone) ([nebula-graph.io][13])
* `lm_studio_wrapper` (or `ollama`) for local models ([LM Studio][25], [Ollama][26])
* `verifier` (hash/Merkle/CID; drift checks)
* `app` (API + Streamlit)
* Optional `gpu-graph` image with **cuGraph** for Louvain if CUDA present ([RAPIDS Docs][27])

---

## 10) Models we’ll ship with (default profiles, all ≤10 GB)

* **RWKV-6/7 \~3B (Q4\_K\_M, GGUF \~2 GB)** → *stance, contradiction, bias flags; long threads* ([Hugging Face][24])
* **Mamba-2 2.7B** → *linear-time summarization/classification* (Transformers/HF has Mamba-2 ready) ([Hugging Face][4])
* **all-MiniLM-L6-v2 / E5-small-v2** → *embeddings/drift* ([Hugging Face][20])
* **BGE-reranker-base** → *top-k precision when it matters* ([bge-model.com][23])
* **Mistral-7B-Instruct (GGUF Q4 ≈5–6 GB)** → *only for synthesis/debate* ([secondstate.io][1])
* **Llama-3-8B (GPTQ-4bit <6 GB)** → *alternative generator* ([Hugging Face][2])

> Quantization formats we support: **GGUF** (llama.cpp family), **GPTQ**, **AWQ**—all established and documented for local serving under low memory. ([Hugging Face][32], [arXiv][33], [proceedings.mlsys.org][34])

---

## 11) Scoring, metrics, acceptance

* **Coverage**: % of output sentences with **valid span-hash + Merkle proof** (target **100%**).
* **Drift**: mean cosine distance vs cited spans (**<0.15**; drop violators) ([Hugging Face][20]).
* **Time-to-result**: corpus→analysis latency (target **<60s** small corpora).
* **Fracture Impact**: 0–100 (documented formula with Louvain Δmodularity and IC spread) ([RAPIDS Docs][27], [Cornell Computer Science][28]).
* **Unity Feasibility**: top-3 bridge paths with parameters (seed set, p(edge), iterations) logged.
* **Reproducibility**: run folder includes **model IDs**, **quant types**, **temps**, **seeds**.

---

## 12) Build plan (6 weeks)

**Week 1–2: Core pipeline**

* Fetchers + Canonicalizer + SHA-256/Merkle + optional IPFS CIDs.
* Nebula schema + loader; embedding + reranker.
* Minimal **analyze** path: retrieve → validate with **RWKV/Mamba-2** classifier → emit **evidence-locked** bullet list. (Generators **off** by default.)

**Week 3–4: Graph intelligence**

* GraphRAG neighborhood prompts; FEUD/MENTIONS extraction. ([Microsoft][31])
* **Louvain** fracture baseline; Streamlit graph; export audit bundle. ([RAPIDS Docs][27])

**Week 5–6: Synthesis & simulator**

* Add **Mistral-7B/Llama-3-8B** for optional pro/con/mediator—**per-sentence citation gate**.
* **Independent Cascade** unity simulator (CPU first, cuGraph optional). ([Cornell Computer Science][28])

---

## 13) Risks & mitigations

* **Marketing vs reality on “trillion edges”**: real capacity depends on cluster size; start **single-node**, leave room to scale. ([nebula-graph.io][13], [Nebula Graph Documentation][36])
* **SSM maturity**: Mamba-2/RWKV are evolving; we scope them to **classification/summarization**, not open-ended reasoning. ([Hugging Face][4], [arXiv][37])
* **GPU env drift for cuGraph**: ship GPU analytics as **optional** feature switch. ([RAPIDS Docs][27])

---

## 14) Why this satisfies your “no >10 GB” and “beyond Transformers” asks

* Every default model is under **10 GB** (many ≤6 GB).
* Core reasoning uses **SSM/RNN (Mamba-2 / RWKV)** and **small encoders**; we only spin up a 7–8B generator when we need polished natural language (and still under 6 GB with Q4/GPTQ). ([Hugging Face][4], [secondstate.io][1])

---

## 15) Nice-to-have (future toggles)

* **PagedAttention/vLLM** if you later host a slightly larger model server-side for batch jobs; improves KV-cache efficiency massively. ([arXiv][38], [vLLM Blog][39])
* **Bamba-9B** (SSM hybrid) if the 10 GB cap is lifted or remote. ([Hugging Face][40])

---

If you want, I’ll generate the starter repo (Docker compose, Nebula schema, ingestion/provenance code, LM Studio & Ollama adapters, Streamlit app) exactly to this spec. Pick your **default generator** (Mistral-7B Q4 or Llama-3-8B 4-bit) and whether you want **RWKV** or **Mamba-2** as the primary validator, and I’ll scaffold it next.

[1]: https://www.secondstate.io/articles/mistral-7b-instruct-v0.3/?utm_source=chatgpt.com "Getting Started with Mistral-7B-Instruct-v0.3"
[2]: https://huggingface.co/astronomer/Llama-3-8B-GPTQ-4-Bit?utm_source=chatgpt.com "astronomer/Llama-3-8B-GPTQ-4-Bit"
[3]: https://arxiv.org/abs/2312.00752?utm_source=chatgpt.com "Linear-Time Sequence Modeling with Selective State Spaces"
[4]: https://huggingface.co/docs/transformers/en/model_doc/mamba2?utm_source=chatgpt.com "Mamba 2"
[5]: https://github.com/state-spaces/mamba?utm_source=chatgpt.com "state-spaces/mamba: Mamba SSM architecture"
[6]: https://arxiv.org/abs/2503.14456?utm_source=chatgpt.com "RWKV-7 \"Goose\" with Expressive Dynamic State Evolution"
[7]: https://huggingface.co/mradermacher/rwkv-6-world-3b-v2.1-GGUF?utm_source=chatgpt.com "mradermacher/rwkv-6-world-3b-v2.1-GGUF"
[8]: https://wiki.rwkv.com/?utm_source=chatgpt.com "RWKV Language Model"
[9]: https://www.ai21.com/blog/announcing-jamba/?utm_source=chatgpt.com "Introducing Jamba: AI21's Groundbreaking SSM- ..."
[10]: https://docs.ai21.com/v4.1/docs/jamba-15-models?utm_source=chatgpt.com "Jamba-1.5 models - AI21 Studio - AI21 Labs"
[11]: https://aws.amazon.com/blogs/aws/jamba-1-5-family-of-models-by-ai21-labs-is-now-available-in-amazon-bedrock/?utm_source=chatgpt.com "Jamba 1.5 family of models by AI21 Labs is now available ..."
[12]: https://huggingface.co/blog/bamba?utm_source=chatgpt.com "Bamba: Inference-Efficient Hybrid Mamba2 Model"
[13]: https://www.nebula-graph.io/?utm_source=chatgpt.com "NebulaGraph: Open Source Distributed Graph Database"
[14]: https://www.nextplatform.com/2021/01/19/third-time-is-the-charm-for-nebula-graph-database/?utm_source=chatgpt.com "Third Time Is The Charm For Nebula Graph Database"
[15]: https://www.microsoft.com/en-us/research/project/graphrag/?utm_source=chatgpt.com "Project GraphRAG - Microsoft Research"
[16]: https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.180-4.pdf?utm_source=chatgpt.com "fips pub 180-4 - federal information processing standards publication"
[17]: https://csrc.nist.gov/pubs/fips/180-4/upd1/final?utm_source=chatgpt.com "FIPS 180-4, Secure Hash Standard (SHS) | CSRC"
[18]: https://docs.ipfs.tech/concepts/content-addressing/?utm_source=chatgpt.com "Content Identifiers (CIDs) - IPFS Docs"
[19]: https://www.cyfrin.io/blog/what-is-a-merkle-tree-merkle-proof-and-merkle-root?utm_source=chatgpt.com "What is a Merkle Tree, Merkle proof, and Merkle Root"
[20]: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2?utm_source=chatgpt.com "sentence-transformers/all-MiniLM-L6-v2"
[21]: https://www.sbert.net/docs/sentence_transformer/pretrained_models.html?utm_source=chatgpt.com "Pretrained Models — Sentence Transformers documentation"
[22]: https://sbert.net/?utm_source=chatgpt.com "SentenceTransformers Documentation — Sentence ..."
[23]: https://bge-model.com/bge/bge_reranker.html?utm_source=chatgpt.com "BGE-Reranker — BGE documentation - bge-model.com"
[24]: https://huggingface.co/tensorblock/SmerkyG_rwkv-6-world-3b-GGUF?utm_source=chatgpt.com "tensorblock/SmerkyG_rwkv-6-world-3b-GGUF"
[25]: https://lmstudio.ai/docs/api?utm_source=chatgpt.com "LM Studio as a Local LLM API Server"
[26]: https://ollama.readthedocs.io/en/api/?utm_source=chatgpt.com "API Reference - Ollama English Documentation"
[27]: https://docs.rapids.ai/api/cugraph/legacy/api_docs/api/cugraph/cugraph.louvain/?utm_source=chatgpt.com "cugraph.louvain"
[28]: https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf?utm_source=chatgpt.com "[PDF] Maximizing the Spread of Influence through a Social Network"
[29]: https://theoryofcomputing.org/articles/v011a004/v011a004.pdf?utm_source=chatgpt.com "[PDF] Maximizing the Spread of Influence through a Social Network"
[30]: https://snap-stanford.github.io/cs224w-notes/network-methods/influence-maximization?utm_source=chatgpt.com "Influence Maximization - SNAP"
[31]: https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/?utm_source=chatgpt.com "GraphRAG: Unlocking LLM discovery on narrative private ..."
[32]: https://huggingface.co/docs/hub/en/gguf-llamacpp?utm_source=chatgpt.com "GGUF usage with llama.cpp"
[33]: https://arxiv.org/abs/2210.17323?utm_source=chatgpt.com "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers"
[34]: https://proceedings.mlsys.org/paper_files/paper/2024/hash/42a452cbafa9dd64e9ba4aa95cc1ef21-Abstract-Conference.html?utm_source=chatgpt.com "AWQ: Activation-aware Weight Quantization for On-Device ..."
[35]: https://huggingface.co/ibm-ai-platform/Bamba-9B-v1/blob/main/bamba-9b.gguf?utm_source=chatgpt.com "bamba-9b.gguf · ibm-ai-platform/Bamba-9B-v1 at main"
[36]: https://docs.nebula-graph.io/2.6.2/8.service-tuning/3.system-design/?utm_source=chatgpt.com "System design suggestions"
[37]: https://arxiv.org/pdf/2406.07887?utm_source=chatgpt.com "An Empirical Study of Mamba-based Language Models"
[38]: https://arxiv.org/abs/2309.06180?utm_source=chatgpt.com "Efficient Memory Management for Large Language Model Serving with PagedAttention"
[39]: https://blog.vllm.ai/2023/06/20/vllm.html?utm_source=chatgpt.com "Easy, Fast, and Cheap LLM Serving with PagedAttention ..."
[40]: https://huggingface.co/ibm-ai-platform/Bamba-9B-v1?utm_source=chatgpt.com "ibm-ai-platform/Bamba-9B-v1"
