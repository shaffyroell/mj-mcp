# SwimScore Blog Workflow

A repeatable, multi-step workflow for producing SEO-optimized SwimScore blog
articles, generating an on-brand hero image, and publishing to Shopify as a
scheduled draft.

**The goal of every article is to drive clients (men and couples) and clinics
to SwimScore.** Every piece must establish scientific credibility, demonstrate
intellectual honesty, and be practically useful, per the `swimscore-content`
skill. This document is the operational runbook that wraps that skill.

---

## 0. Prerequisites (per session)

- **FLUX image generation** requires `BFL_API_KEY` (Black Forest Labs) in the
  environment, and the environment's network policy must allow outbound HTTPS
  (Network access = Full, or Custom allowlisting `api.bfl.ai` and `*.bfl.ai`).
- **Shopify** must be connected (MCP). Store: SwimScore, `www.myswimscore.com`.
- The **`swimscore-content` skill** is the source of truth for voice, research
  standards, and article structure. Always follow it. This runbook never
  overrides it. It is **committed in this repo** at
  `.claude/skills/swimscore-content/SKILL.md`, so it is available automatically
  whenever the repo is cloned (no separate attachment required).

---

## 1. Discover existing content (avoid duplicates, gather link targets)

Query the Shopify Admin API for every published article so you do not duplicate
a topic and so you can collect internal-link targets and match the house image
style.

```graphql
query BlogArticles {
  blogs(first: 5) {
    edges { node { id handle title
      articles(first: 50, reverse: true) {
        edges { node { id title handle publishedAt tags image { url altText } } }
      }
    } }
  }
}
```

- The main blog is **News** (`gid://shopify/Blog/92195225782`, handle `news`).
  Publish there unless told otherwise.
- Note which topics are already covered. Read 1-2 full article bodies (query the
  `body` field by article ID) to re-calibrate voice before writing.

## 2. Choose the topic

Pick a topic that is (a) not already covered, (b) high SEO value, and (c) good
for internal linking and the client + clinic goal. Prioritize the
`swimscore-content` skill's "not yet started, high priority" list (clinical and
lifestyle topics: enclomiphene [done], varicocele, heat exposure, alcohol
[done], obesity, sleep, exercise, IVF/ICSI, how to read your results), and the
in-progress series (Hormone Series next: Prolactin done, Estradiol done; Sperm
Parameter Series Part 5: TMSC / putting parameters together).

State the chosen topic and a one-line justification before writing. If the user
named a topic, use it.

## 3. Research (real sources only)

Follow the skill's Research Standards. Read actual studies (PubMed, PMC,
guidelines: AUA, EAU, ASRM, WHO). For deep/clinical topics, run a dedicated
research pass and produce a citable evidence brief with:

- Specific study design, sample size, and numeric findings.
- Citations in the format `(Author et al., Journal Name, Year)`.
- **Explicit honesty flags**: what is thin, contested, or unverified. Do not cite
  claims you could not verify in a primary source. Never overclaim pregnancy or
  live-birth benefit. Apply the Henriksen 2025 rule where supplements come up.

## 4. Write the article (invoke the `swimscore-content` skill)

Use the skill's structure template for the content type (clinical explainer,
sperm-parameter series, hormone series, lifestyle, or product/testing). Hard
rules, checked before finishing:

- **NO EM-DASHES and no en-dashes. Zero. Scan explicitly.** Use commas, colons,
  periods, or restructure.
- Plain English. Explain every mechanism and term in the same breath. Prose, not
  bullet lists, for practical advice.
- Confident where evidence supports it, plainly honest where it does not.
  Include a "what we are more skeptical about" beat where relevant.
- No supplement-brand language ("boost", "supercharge", "game changer"), no
  wellness clichés ("fertility journey"), no marketing superlatives.
- **Internal links (SEO + the client/clinic goal):** link naturally to relevant
  published articles and pages. Known targets:
  - Hormone series: `/blogs/news/what-your-fsh-level-is-actually-telling-you-about-your-fertility`,
    `/blogs/news/what-your-lh-level-reveals-about-your-testosterone-and-fertility`,
    `/blogs/news/what-your-testosterone-level-actually-tells-you-about-your-fertility`,
    `/blogs/news/what-your-estradiol-level-reveals-about-your-fertility`,
    `/blogs/news/what-your-prolactin-level-is-telling-you-about-your-fertility`
  - Parameters: `/blogs/news/does-your-sperm-count-actually-matter-what-the-research-shows-on-concentration`,
    `/blogs/news/does-sperm-dna-fragmentation-actually-matter-heres-what-the-research-shows`,
    `/blogs/news/what-does-sperm-morphology-actually-tell-you-an-honest-look-at-the-research`
  - Credibility: `/blogs/news/what-is-a-clia-certified-lab-and-why-does-it-matter-for-semen-testing`
  - **Client CTA (product):** `/products/swimscore-complete` (the full panel:
    semen parameters + DNA fragmentation + hormones). Other products:
    `/products/swimscore-essential`, `/products/swimscore-advanced`.
  - **Clinic CTA (required where natural):** `/pages/for-clinics`.
  - Other pages: `/pages/what-we-measure`, `/pages/how-it-works`, `/pages/couples`.
- **Closing lines** (italic), per skill:
  - A clinic CTA line pointing to `/pages/for-clinics` when the topic suits it.
  - For clinical topics: a "not medical advice" line.
  - Always end with: *SwimScore uses CLIA-certified labs for all semen analysis
    and hormone testing, assessed against WHO 6th Edition clinical thresholds.*
- Write the body as clean semantic HTML: `<p>`, `<h2>` for section headings,
  `<a href>`, `<em>`, `<hr>`. Do not repeat the title inside the body.
- Also produce: an **SEO meta title** (~55-60 chars), an **SEO meta description**
  (~150-160 chars), a **URL handle**, and a 1-2 sentence **summary**.

**Required quality gate:** before finalizing, run
[`CONTENT_CHECKLIST.md`](./CONTENT_CHECKLIST.md) end to end and fix anything that
fails. It verifies the four things that matter most: we are not pushing meds or
supplements, everything we say is true to the cited sources, we are genuinely
helpful for navigating the mixed research and online noise, and it is simple
enough for any everyday man to understand.

## 5. Generate the hero image (FLUX)

Use `flux_generate.py` (BFL FLUX `flux-pro-1.1-ultra`, aspect ratio 16:9).

```bash
uv run python flux_generate.py "<prompt>" --n 3 --ar 16:9 --seed <n> --out <dir>
```

**Image rules (hard):**

- **People: men only, or a man with a woman (heterosexual couple). SwimScore is
  a male-fertility brand. Never same-sex couples. Never women-only.**
- **Relatable and realistic, not fashion models.** Ordinary, approachable,
  everyday men in their 30s-40s, natural skin, normal builds. Warm and quietly
  hopeful, not somber and not glossy/idealized.
- **House aesthetic:** premium but understated health-brand photography, soft
  natural/warm light, muted natural palette, shallow depth of field,
  photorealistic, editorial. Subject framed to one side with clean negative
  space works well for the blog card.
- **Recurring house scenes** (match these): confident/relatable man at home or
  outdoors in warm light; a man with his partner; a man in consultation with a
  warm doctor; a man on a telehealth call; a scientist/lab context. Choose the
  scene that fits the article.
- **Reject** any image with visible text/logo artifacts (garbled lab-coat text,
  signage), extra fingers, or other obvious AI defects.
- Generate at least 3 variations across 1-2 concepts, review them, and pick the
  single best fit. Then resize/optimize to the house hero size **1456 x 816**
  and save as an optimized JPG (quality ~88, target < 200 KB) for page speed:

```bash
uv run --with pillow python - <<'PY'
from PIL import Image
Image.open("<src>.png").convert("RGB").resize((1456,816), Image.LANCZOS).save("<dst>.jpg","JPEG",quality=88,optimize=True)
PY
```

## 6. Publish to Shopify (scheduled draft)

1. **Stage-upload the image**: `stagedUploadsCreate` with
   `{ resource: IMAGE, filename, mimeType: "image/jpeg", httpMethod: POST }`,
   then POST the file (with all returned parameters, file field last) to the
   returned `url`; use the returned `resourceUrl` as the article image URL.
2. **Create the article** with `articleCreate`:
   - `blogId`: News blog id above. `author: { name: "SwimScore" }`.
   - `body`: the HTML. `summary`: the teaser HTML. `handle`: the SEO handle.
   - `tags`: relevant topic tags.
   - `image`: `{ url: <resourceUrl>, altText: <descriptive, relevant alt text> }`.
   - **SEO metafields**:
     `{ namespace: "global", key: "title_tag", type: "single_line_text_field", value: <meta title> }`
     and the same with `key: "description_tag"` for the meta description.
   - **Draft + schedule**: create with `isPublished: false` (a hidden draft for
     review) and `publishDate` set to the intended posting time (ISO 8601 UTC).
     **Gotcha:** `articleUpdate` re-evaluates the publish state, so if you later
     edit the article you MUST pass `isPublished: false` again or Shopify can
     flip the draft live (or schedule it) when a `publishDate` is present. Always
     read back `isPublished` and confirm it is `false`.
     To arm true auto-publish at that time, set `isPublished: true` (Shopify then
     treats a future `publishDate` as scheduled). Default policy: leave as a
     hidden draft and only arm auto-publish after the content has been reviewed,
     unless the user has authorized auto-publish.
3. **Verify** by reading back `id, handle, isPublished, publishedAt, image.url,
   metafields`. The image URL should be on `cdn.shopify.com`.

## 7. Scheduling / the routine

A Claude routine (scheduled trigger) can run this whole workflow on a cadence.
Each run should: discover existing articles, pick the next priority topic,
research, write per the skill, generate a compliant hero image, and create the
Shopify draft with SEO set and a `publishDate` on the desired posting slot.

**Publish policy** (set by the user):
- *Draft for review* (safer for medical content): create `isPublished: false`
  and notify for human review before it goes live.
- *Auto-publish*: create scheduled (`isPublished: true`, future `publishDate`).

Recommended posting slot: a weekday morning US Eastern. Keep a buffer between
draft creation and the publish date for review.

---

## Quick reference

| Item | Value |
| --- | --- |
| Store | SwimScore, `www.myswimscore.com` |
| News blog id | `gid://shopify/Blog/92195225782` (handle `news`) |
| Product (full panel) | `/products/swimscore-complete` (`gid://shopify/Product/8501242658998`) |
| Clinic page | `/pages/for-clinics` |
| Hero image size | 1456 x 816, optimized JPG |
| Image people rule | Men, or man + woman couple. Never same-sex or women-only. |
| Image feel | Relatable, realistic, everyday. Not fashion models. |
| SEO meta title | metafield `global.title_tag` (~55-60 chars) |
| SEO meta description | metafield `global.description_tag` (~150-160 chars) |
| Hard writing rule | No em-dashes or en-dashes, ever |
| Every article ends with | italic CLIA / WHO 6th Edition line |

## Key clinical facts to always get right (from the skill)

WHO 6th Edition: progressive motility 32%, concentration 16 M/mL, total count
39 M/ejaculate, morphology 4% (Kruger). DFI: <15% good, 15-30% moderate, >30%
high. Spermatogenesis cycle ~72 days, so always say "at least 12 weeks" for
intervention protocols. Intratesticular testosterone is 50-100x serum. LH
~1.5-9.3 mIU/mL, FSH ~1.0-7.6 mIU/mL. Enclomiphene is off-label, not
FDA-approved for male infertility.
