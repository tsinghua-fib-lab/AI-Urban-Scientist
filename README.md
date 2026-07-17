# AI Urban Scientist
<p align="center">
  <img src="img1.png" alt="描述" width="100%" />
</p>

> **An autonomous AI research scientist for urban science - from topic to publication.**

Urban AI Scientist is an end-to-end automated research pipeline designed forthe urban science domain. Given a research topic, it independently conducts thefull research lifecycle: literature-grounded idea generation, open-data discovery and acquisition, experimental design and execution, statistical analysis, figure generation, and Nature-format paper writing with PDF compilation. The system embodies the AI Scientist paradigm, enabling autonomous hypothesis formation, empirical validation, and scholarly communication in urban science.

🌐 **Live Demo**: [https://cocoa-heap-turbulent.ngrok-free.dev](https://cocoa-heap-turbulent.ngrok-free.dev)

> 💬 [中文文档 →](./README_zh.md)

*New 2026.07.17* **AI-Urban-Sci Skill v1.0 is now officially released!** This release integrates the full capabilities of our platform and is fully compatible with leading development tools including Claude Code, Codex, and Qoder, thereby empowering scientific research workflows. We are committed to ongoing updates and long-term maintenance to ensure sustained performance and feature enhancements.

---

## Authors

Authors are listed alphabetically by first name.

| Author | Affiliation |
|--------|-------------|
| **Ao Xu**  | Zhongguancun Academy; Jilin University |
| **Jiankun Zhang**  | Zhongguancun Academy; Jilin University |
| **Jingzhi Wang**  | Zhongguancun Academy; East China Normal University |
| **Runwen You**  | Zhongguancun Academy; Jilin University |
| **Tong Xia**  | Tsinghua University; Zhongguancun Academy |
| **Yong Li**  | Tsinghua University; Zhongguancun Academy |

---

## Pipeline Overview

```
Research Topic
  │
  ▼
┌──────────────────────────────────────────────┐
│  Phase 1: Idea Generation                     │
│  Generate novel research idea with literature │
│  grounding and related datasets               │
└──────────────────────────────────────────────┘
  │  (User review: Continue · Regenerate · Cancel)
  ▼
┌──────────────────────────────────────────────┐
│  Phase 2: Data Seeking                        │
│  Search, discover, and download open datasets  │
│  for the proposed study                        │
└──────────────────────────────────────────────┘
  ▼
┌──────────────────────────────────────────────┐
│  Phase 3: Paper Planning                      │
│  Build a claim-first paper plan with evidence │
│  graph, task queue, and figure blueprints      │
└──────────────────────────────────────────────┘
  ▼
┌──────────────────────────────────────────────┐
│  Phase 4: Paper Writing                       │
│  Execute experiments → generate figures →     │
│  write LaTeX → compile PDF (Nature format)    │
└──────────────────────────────────────────────┘
```

Four phases run sequentially with real-time progress streaming.

---

## Getting Started

### 1. Open the Website

Visit the [live demo URL](https://cocoa-heap-turbulent.ngrok-free.dev).

### 2. Authentication

Two ways to access:

| Method | Description |
|--------|-------------|
| **Passphrase** | Enter the shared access key. API Key field will be hidden automatically. |
| **Own API Key** | Provide your own API Key + Base URL (any OpenAI-compatible endpoint). |

### 3. Choose a Method

| Method | Description |
|--------|-------------|
| **CAMP** | Literature-driven: retrieves related papers first, then generates grounded ideas |
| **SEMM** | Direct generation: creates ideas from the topic without prior retrieval |
| **FAST** | Lightweight LLM mode: fastest, no backend API dependency |

### 4. Select a Model (Optional)

When accessing via passphrase, you can switch between available models:

`claude-sonnet-4-6` · `glm-5.1` · `qwen3.5-plus` · `qwen3.7-max` · `mimo-v2.5-pro` · `deepseek-v4-pro` 

Default: `claude-sonnet-4-6`.

### 5. Enter Your Research Topic

Both English and Chinese are supported. Examples:

- `Urban flood prediction using satellite imagery`
- `基于 BRFSS 数据集量化高温与睡眠不足的关系`
- `Impact of ride-hailing on urban commuting efficiency`

### 6. Launch

Click **Launch** to start the pipeline:

- Real-time progress log via SSE streaming
- Each phase highlights on completion
- Downloadable artifacts after each stage

### 7. Idea Review

After Phase 1, the system presents an idea preview (title + abstract):

| Action | Description |
|--------|-------------|
| **Continue** | Accept and proceed to data seeking |
| **Regenerate** | Clear current idea and try again |
| **Cancel** | Stop the entire pipeline |

Auto-continues after 30 seconds of inactivity.

### 8. Download Artifacts

| Phase | Artifact |
|-------|----------|
| Idea | Research idea document (Markdown) |
| Data | Dataset download report |
| Plan | Paper plan with experiment design |
| Paper | Final compiled PDF (Nature format) |

---

## Example Papers

See the [`examples/`](examples/) directory for complete papers generated by the system,
including final PDFs and (where available) full job directories with intermediate outputs
(ideas, data reports, plans, and figures).

---

## Architecture

```
┌──────────────┐     SSE      ┌──────────────────┐
│   Frontend   │ ◄──────────► │   FastAPI Backend │
│  (Vue 3 SPA) │              │                   │
└──────────────┘              └────────┬──────────┘
                                       │
                              4× Sequential AI Agent Runs
                              (streaming JSON mode)
                                       │
                              ┌────────┼────────┐
                              ▼        ▼        ▼
                          Idea     Data     Paper
                        Generator Seeker  Writer
```

- **Frontend**: Vue 3 + Vite, single-page application
- **Backend**: FastAPI with Server-Sent Events for real-time streaming
- **Pipeline Engine**: Four sequential AI agent runs, each executing a specialized skill
- **Paper Compilation**: LaTeX (`nature.cls` template) + `latexmk`
- **Public Access**: ngrok (fixed domain) / Cloudflare Tunnel

---

## Notes

- **One job at a time** — a concurrency lock ensures only one pipeline runs simultaneously
- **Keep the browser tab open** — disconnecting cancels the running job
- **Estimated duration**: 30–60 minutes end-to-end (Idea ~5 min → Data ~10 min → Plan ~10 min → Paper ~20–40 min)
- **API cost**: ~$5–15 for a full run with your own API key (varies by model and topic complexity)
- **Storage**: Artifacts are stored server-side by job ID. Download promptly.

---

## FAQ

**Q: The page says "another job is running".**  
A: Wait for the current job to finish and try again. Only one pipeline runs at a time.

**Q: Can I resume a failed job?**  
A: Yes. The system skips completed phases on retry, so it picks up from where it left off.

**Q: Are Chinese topics supported?**  
A: Yes, both English and Chinese topics work well.

**Q: Do I need an Anthropic API key?**  
A: No. Any OpenAI-compatible API endpoint works. Just provide your API Key and Base URL.

**Q: What format is the final paper?**  
A: A single-file LaTeX document following Nature journal format, plus a compiled PDF.

---

## License

MIT

---

## Contact

Need a passphrase or have questions? Open an [Issue](../../issues).
