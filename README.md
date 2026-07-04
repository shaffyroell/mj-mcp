# SwimScore Blog Content Automation

This repository powers **SwimScore's automated blog content workflow**. On a
schedule, it researches a male-fertility topic, writes an SEO-optimized article
in the SwimScore voice, generates an on-brand hero image with FLUX, and creates
a **draft** post in Shopify for human review.

The entire goal of every article is to **drive clients (men and couples) and
clinics to SwimScore**.

> The complete, authoritative runbook is **[`SWIMSCORE_BLOG_WORKFLOW.md`](./SWIMSCORE_BLOG_WORKFLOW.md)**.
> Read it first. This README is the summary.

---

## What runs, and when

A **Claude Routine** (scheduled trigger) fires **twice a week, Tuesday and
Thursday at 13:30 UTC (~9:30am US Eastern)**. Each run:

1. Reads `SWIMSCORE_BLOG_WORKFLOW.md` and follows the `swimscore-content` skill.
2. Queries the Shopify **News** blog and picks the next priority topic not yet
   covered.
3. Researches it against real primary sources and writes the article to spec
   (no em-dashes, plain English, honest about uncertainty, internal links,
   client + clinic CTAs).
4. Generates a compliant hero image (see image rules below) and optimizes it to
   1456x816.
5. Creates the article in Shopify as a **hidden draft** (`isPublished: false`)
   with SEO meta title/description, tags, alt text, and a target `publishDate`.
6. Notifies for review. **It never auto-publishes.**

## Repository contents

| File | Purpose |
| --- | --- |
| `SWIMSCORE_BLOG_WORKFLOW.md` | The authoritative step-by-step runbook. |
| `flux_generate.py` | Generates hero images via the Black Forest Labs FLUX API. |
| `pyproject.toml` | Python dependencies for the image script (`httpx`, `pillow`). |

## Image rules (hard requirements)

- **People: men only, or a man with a woman (heterosexual couple).** SwimScore
  is a male-fertility brand. Never same-sex couples, never women-only.
- **Relatable and realistic, not fashion models.** Everyday men in their 30s to
  40s, natural, warm, and quietly hopeful.
- Premium but understated health-brand aesthetic, warm natural light, 16:9,
  optimized to 1456x816.

## Generating an image manually

```bash
export BFL_API_KEY=...   # Black Forest Labs API key
uv run python flux_generate.py "your prompt" --n 3 --ar 16:9 --out images/
```

## Prerequisites for the routine to run

Because each scheduled run starts a **fresh** cloud session, these must be
available to it, not just to an interactive session:

1. **`BFL_API_KEY`** set in the environment's persistent variables (for FLUX).
2. **Shopify MCP** connected (to create the draft).
3. The **`swimscore-content`** skill. This is now **committed in this repo** at
   `.claude/skills/swimscore-content/SKILL.md`, so it loads automatically
   whenever the repo is cloned. No separate attachment needed.
4. **Network access** allowing `api.bfl.ai` (Full, or Custom allowlisting
   `api.bfl.ai` and `*.bfl.ai`).

The routine self-checks these and stops with a report if any is missing, rather
than producing a broken post.

## License

Licensed under the GNU General Public License v3.0 (GPL-3.0). See `LICENSE`.
