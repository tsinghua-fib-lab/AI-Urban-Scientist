# Urban AI Scientist — Idea Creator Skill

A Claude Code skill that generates urban science research ideas using your own LLM API key.

---

## Installation

```bash
bash skills/install_user_llm_skill.sh
```

Or pass credentials directly:

```bash
bash skills/install_user_llm_skill.sh \
  --key sk-xxxxxxxx \
  --base https://api.openai.com/v1 \
  --model gpt-4o-mini
```

Credentials are saved to `~/.claude/skills/idea-creator-user-llm/credentials.json`. Any OpenAI-compatible provider (DeepSeek, Qwen, SiliconFlow, etc.) is supported.

A Semantic Scholar API key is optional but recommended to avoid rate limits when using `novelty`.

---

## Methods

| Method | API Key | Backend | Description |
|--------|:-------:|:-------:|-------------|
| **CAMP** | Yes | Yes | Retrieves related papers from the database → CAMP hypothesis generation → refined idea. Highest quality. |
| **DIRECT** | No | No | Claude-native reasoning with optional web search. No credentials needed. |
| **FAST** | Yes | No | Calls your LLM directly with a built-in urban science prompt. One idea, fast. |
| **novelty** | Yes | Yes | Searches Semantic Scholar / arXiv for related papers, analyzes relevance, and appends a `## Novelty Check` section to an existing idea `.md` file. |

---

## Usage

### Generate an idea

```
/idea-creator-user-llm <METHOD> [options] <research topic>
```

```
/idea-creator-user-llm CAMP urban heat island and public health
/idea-creator-user-llm CAMP --paper_domain Economics --retrieval_limit 8 urbanization and inequality
/idea-creator-user-llm DIRECT climate change and urban resilience
/idea-creator-user-llm FAST shared mobility and urban vitality
```

### Check novelty of an existing idea

```
/idea-creator-user-llm novelty <path/to/idea.md>
/idea-creator-user-llm novelty --source arxiv <path/to/idea.md>
```

The `.md` file must contain a `## Title` and `## Abstract` section (the default output format of CAMP / DIRECT / FAST). The novelty summary is appended in-place — the original content is not modified.

---

## Parameters

| Parameter | Default | Method | Description |
|-----------|---------|--------|-------------|
| `--temperature` | `0.5` | All | Generation randomness (0.0–2.0). Higher = more creative. |
| `--paper_domain` | `Urban Science` | CAMP | Retrieval domain: `Urban Science`, `Economics`, `Finance`, `all`. |
| `--retrieval_limit` | `5` | CAMP | Max papers retrieved per query. |
| `--retrieval_method` | `mixture` | CAMP | Retrieval strategy: `mixture`, `dense`, `sparse`. |
| `--source` | `semantic` | novelty | Paper search source: `semantic` (Semantic Scholar) or `arxiv`. |
