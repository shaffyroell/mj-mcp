# SwimScore Blog Workflow

A repeatable, multi-step workflow for producing SEO-optimized SwimScore blog
articles, generating an on-brand hero image, and publishing to Shopify as a
scheduled draft.

**The goal of every article is to drive clients (men and couples) and clinics
to SwimScore.**

**Which document wins.** This runbook is authoritative for topic choice
(Part 1), the writing rules (Part 2), and article structure, product tier,
links, and closing lines (Part 3). The `swimscore-content` skill
(`.claude/skills/swimscore-content/SKILL.md`) adds voice detail, worked
examples, the per-content-type section orders, and key clinical facts. If the
skill and this runbook ever disagree, follow this runbook.

---

## 0. Prerequisites (per session)

- **FLUX image generation** requires `BFL_API_KEY` (Black Forest Labs) in the
  environment, and the environment's network policy must allow outbound HTTPS
  (Network access = Full, or Custom allowlisting `api.bfl.ai` and `*.bfl.ai`).
- **Shopify** must be connected (MCP). Store: SwimScore, `www.myswimscore.com`.
- **Live price checks** (Part 2, Prices) need outbound web access to the pages
  being priced (for example `www.myswimscore.com` and `givelegacy.com`). If a
  price cannot be checked live in this run, follow the Prices rules for leaving
  it out. Never fall back to a remembered price.
- The **`swimscore-content` skill** is committed in this repo at
  `.claude/skills/swimscore-content/SKILL.md`.

---

## 1. Discover existing content

Query the Shopify Admin API for every article on the blog, published or draft.
Always query live. No document in this repo tracks what is already published,
and none should ever be edited to track it.

```graphql
query BlogArticles {
  blog(id: "gid://shopify/Blog/92195225782") {
    articles(first: 100, reverse: true) {
      pageInfo { hasNextPage endCursor }
      nodes {
        id title handle publishedAt isPublished tags
        image { url altText }
        notes: metafield(namespace: "swimscore", key: "draft_notes") { value }
      }
    }
  }
}
```

- The main blog is **News** (`gid://shopify/Blog/92195225782`, handle `news`).
  Publish there unless told otherwise.
- Paginate until `hasNextPage` is false.
- Read 1-2 full article bodies (query `body` by article ID) to re-calibrate
  voice before writing.

---

## PART 1: CHOOSE THE TOPIC

1. Fetch every article in the Shopify News blog (published and draft), as in
   step 1 above. Never keep a saved list of covered topics.

2. Choose a topic from the categories below. Use common sense: pick something a
   man worried about his fertility would realistically search for, and that the
   blog doesn't already answer.

   - **A. Cost and coverage:** test prices, clinic vs at-home, insurance. No
     HSA/FSA articles (see the HSA/FSA rule in Part 2).
   - **B. Testing options and accuracy:** kit types, reliability, how to prepare,
     sperm freezing
   - **C. Medications, supplements and substances:** their effect on sperm
   - **D. What a specific result number means**
   - **E. Symptoms and conditions** people search by name or appearance
   - **F. Life events and timing:** vasectomy, miscarriage, before IVF or trying,
     regeneration, illness
   - **G. Myths and everyday "does X affect sperm" questions**
   - **H. Lifestyle and environment:** exercise, sleep, diet, weight, heat,
     alcohol, smoking, microplastics and chemicals

   **Topic ideas** (a starting point, not a queue; new topics in the same spirit
   are welcome):

   - **A:** DNA fragmentation test cost; semen analysis cost clinic vs at-home;
     sperm freezing cost
   - **B:** count-only kits vs mail-in lab tests; how long to abstain before a
     semen analysis; sperm freezing and banking
   - **C:** hCG on TRT; finasteride; creatine; Ozempic/Mounjaro; SSRIs; anabolic
     steroids and prednisone; ashwagandha; tongkat ali; caffeine; lubricants
   - **D:** morphology 1%, 2%, 3%; sperm count needed to get pregnant; DFI of 20%
     or 35%; low semen volume
   - **E:** low sperm count signs and causes; watery or thick semen; yellow,
     brown or bloody semen; how common male infertility is
   - **F:** semen analysis after vasectomy; miscarriage and sperm; how long sperm
     takes to regenerate; testing before IVF; fever or COVID and sperm
   - **G:** phone in pocket; laptop on lap; boxers vs briefs; daily ejaculation
     and sperm count; soy
   - **H:** microplastics and sperm; exercise and cycling; endocrine disruptors
     and PFAS; sleep; diet

3. Rules for picking:
   - **Variety:** don't use the same category as either of the last 2 articles.
     "Last 2" means the two most recent articles by `publishedAt` (or scheduled
     publish date), drafts included. Read their category from the
     `swimscore.draft_notes` metafield; for older articles that have no note,
     infer the category from the title and body.
   - **No repeats:** skip any topic where an existing article already answers
     the same question. Same subject isn't enough to count as covered: "What is
     DFI?" does not cover "How much does a DFI test cost?". If unsure, open the
     article body to check.
   - **Overlap:** if a new topic touches a live article, narrow the new one to
     its own question and link to the live one.
   - **Never stop for lack of ideas:** if the topic ideas run out, come up with a
     new question in the category with the fewest recent articles.

4. **Draft notes (not the article):** write one line giving the category and
   why this topic was picked, for example
   `C: Medications. "Does creatine affect sperm" is a common search and no live article answers it.`
   Shopify articles have no built-in notes field, so store this line in the
   article metafield `swimscore.draft_notes` (type `single_line_text_field`).
   It is never shown in the article body. Also state it in the run's final
   report.

---

## PART 2: WRITE THE ARTICLE

### Stance

- Read across mixed research and give an honest, practical view.
- Default structure of the argument: what we know, what we don't know, why it's
  still worth acting on.
- **Myth articles (category G):** state the claim, give the verdict in the first
  paragraph (holds up / partly holds up / doesn't hold up / unclear), then the
  evidence. Follow the extra-care rules for myth verdicts below.

### Voice

- A knowledgeable friend who has read the studies, writing as "we".
- Confident where evidence is strong, plain about uncertainty.
- Explain every technical term in plain English the first time it appears.
- Test: if a paragraph could appear unchanged in a textbook, rewrite it.

### Research rules

- Primary sources only. Never cite news coverage or blogs.
- Every finding states study design and sample size in the same sentence.
- Every claim cites one specific study: Author et al., Journal, Year, with a
  PubMed or DOI link.
- Label weak or contested evidence as weak or contested.
- If a claim can't be verified, delete it.

### Pregnancy rule

- Never claim a pregnancy or live-birth benefit without direct evidence. Better
  sperm numbers do not equal more pregnancies.
- Any article that discusses supplements must state the Henriksen 2025 finding:
  across 50 trials, no supplement improved pregnancy or live-birth rates, though
  some improved motility. Do not use it to dismiss the topic.

### No pushing treatments

- The only calls to action: know your numbers, get tested, talk to a clinician.
- Describe prescription treatments as clinician-managed.
- Every article includes a section titled **"What we are more skeptical about"**.
- **Symptom articles (category E):** state when to see a doctor promptly (e.g.
  blood in semen with pain, a testicular lump). Never say testing replaces an
  exam. Follow the extra-care rules for symptoms below.

### Prices (any article that mentions a price)

- Check every price live during this run. Never use a price from memory or an
  earlier article.
- Include "Prices checked [Month Year]".
- Third-party clinic or lab prices: give a sourced range and label it as such.
- **DNA fragmentation price comparison:** allowed ONLY if both prices below were
  checked live this run. Otherwise leave the comparison out entirely.
  - SwimScore Advanced: `/products/swimscore-advanced`
  - Legacy: `givelegacy.com` (the product that includes DNA fragmentation)

  Write it as a range ("At-home DNA fragmentation testing ranges from $X
  (SwimScore Advanced) to $Y (Legacy)") and state what each price includes.
  Then state that clinic DNA fragmentation testing is often more expensive than
  both, citing at least one sourced clinic price. If no clinic price can be
  sourced, write: "Clinic pricing varies and is often higher."
- Name no other competitors unless verified the same way.
- Follow the extra-care rules for pricing below.

### HSA/FSA

- Never write an article about HSA/FSA eligibility or make HSA/FSA the subject
  of a section.
- The only permitted mention: SwimScore tests are cash pay, though often
  HSA/FSA eligible. Use that wording (or a close equivalent) and nothing more
  specific: no claims about a particular plan, reimbursement amounts, or tax
  treatment.

### Extra care: pricing, medications, symptoms, myth verdicts

These four areas carry the most legal, medical, and trust risk. Speak plainly,
but never trade accuracy or safety for a cleaner sentence. When in doubt, leave
the claim out.

**Pricing and product claims**
- Every price comes from the source page, read live in this run. List each
  price with its source URL and the date checked in the run's final report so
  a reviewer can verify it.
- Compare like with like. State what each price includes (which tests, lab
  report, shipping, consult). If you cannot confirm what a competitor's price
  includes, leave the comparison out.
- Facts only about competitors: price and what is included. No judgments on
  their quality, accuracy, or service.
- No "cheapest", "best value", "save X%", "lowest price", discount codes, or
  promotional language.
- Say prices can change: "Prices checked [Month Year] and may have changed."
- What a SwimScore tier measures (closing line 1 and the body product link)
  must come from that product's page, read live in this run. Never describe
  a tier's contents from memory.

**Medication and substance articles (category C)**
- Near the top of the article, in plain words: "Do not stop, start, or change
  the dose of a prescribed medication without talking to the doctor who
  prescribed it." Repeat it in the FAQ.
- No dosing advice, no cycling or "post-cycle" protocols, no sources or where
  to buy, no compounded or grey-market products.
- State regulatory status exactly: what the drug is FDA-approved for, and when
  a use is off-label. Do not imply a drug is approved for male infertility
  unless it is.
- Weigh the reason for the medication. For antidepressants, hair-loss, weight,
  or other drugs, say plainly that the condition being treated matters too,
  and that alternatives are a conversation for the prescriber.
- Anabolic steroids and non-prescribed testosterone: describe the harm to
  sperm production plainly. No harm-reduction protocols.
- Supplements: say they are not regulated like drugs and products vary, and
  state the Henriksen 2025 finding.
- Do not call an association a cause. Most medication data is observational;
  say so.

**Symptom articles (category E)**
- Put a "When to see a doctor" section in the first half of the article, not
  only in the FAQ. Say plainly that these need a prompt doctor visit: a lump,
  swelling, or change in a testicle, even if painless; testicular pain;
  blood in semen that keeps coming back, or comes with pain, fever, or trouble
  urinating, or in a man over 40.
- Never diagnose and never say "this is nothing to worry about". Say what
  common harmless causes exist, then that only an exam can rule out the
  serious ones.
- Say plainly that an at-home semen test is not designed to diagnose
  infection, cancer, or the cause of a symptom, and does not replace an exam.
- Keep the product link low-key and after the doctor guidance.

**Myth verdicts (category G)**
- The verdict must match the strength of the evidence, and the verdict sentence
  says how strong that evidence is (for example "doesn't hold up, based on
  several large studies" or "unclear, the studies are small and conflicting").
- "Doesn't hold up" only when good studies looked and found no meaningful
  effect. No studies is not proof of no effect: use "unclear".
- "Holds up" only when the effect is consistent across decent studies, and
  say how big it is in plain terms.
- Never turn a verdict into permission for something risky (for example, "the
  laptop myth doesn't hold up, so heat doesn't matter").

### Fixed facts (use this exact wording)

- WHO 6th Edition thresholds: 32% progressive motility, 16 million per mL,
  39 million total, 4% morphology.
- DNA Fragmentation Index (DFI) bands: below 15%, 15 to 30%, above 30%.
- About 72 days to make sperm, so "at least 12 weeks" before retesting.
- Enclomiphene is used off-label.

### Banned

- Em-dashes and en-dashes. No exceptions. Scan explicitly before finishing.
- "boost", "supercharge", "game changer", and similar supplement-marketing words.
- "fertility journey" and other wellness cliches.
- "industry-leading", "revolutionary", and other hype.
- Defensive or hedging openers.

---

## PART 3: STRUCTURE

### Title

- Use the reader's question in their own words, e.g. "Does Creatine Affect
  Sperm?"
- Do not use "What the Research Actually Shows" if the newest live article
  already uses it.

### Order of the article

1. **Key Takeaways:** exactly three sentences.
2. **Body:** question headings, each answered in its first sentence. Prose, no
   bullet lists. Use the fixed section order for the content type (hormone,
   sperm-parameter, clinical, lifestyle, testing) from the skill.
3. **FAQ.**
4. **Numbered References.**
5. **Closing lines, in italics, in this order:**
   1. *Want to know your own numbers? [SwimScore &lt;Tier&gt;](&lt;tier URL&gt;)
      measures &lt;what it tests&gt; from home.*
   2. *If you're a clinic looking to offer fertility testing to your patients,
      [sign up here](/pages/for-clinics).*
   3. *Related reading:* 1 or 2 live SwimScore articles on the closest topic.
   4. Optional, for articles in a numbered series: *This is Part [N] of the
      SwimScore [Series]. Next up: [topic].* Find N from the live articles.
      Name a real, not-yet-covered topic in that series; never promise a date.
   5. Not-medical-advice line.
   6. *SwimScore uses CLIA-certified labs for all semen analysis and hormone
      testing, assessed against WHO 6th Edition clinical thresholds.*

Body HTML is clean and semantic: `<p>`, `<h2>`, `<a href>`, `<em>`, `<hr>`
(the Key Takeaways, FAQ, and References may use `<ul>`/`<ol>`). Do not repeat
the title in the body.

### AI-citation rules

- Every key claim must make sense when quoted on its own.
- Name SwimScore explicitly in key fact sentences.

### Product tier (apply the first rule that matches)

1. Article involves **hormones** (TRT, hCG, steroids, GLP-1/weight,
   testosterone, full workup) -> **SwimScore Complete**,
   `/products/swimscore-complete`
2. Article involves **DNA damage** (DFI, miscarriage, before IVF, paternal age,
   comparing at-home tests) -> **SwimScore Advanced**,
   `/products/swimscore-advanced`
3. **Everything else** -> **SwimScore Essential**, `/products/swimscore-essential`

### Product links

- **Exactly two product links per article, both to the tier chosen above:**
  1. One in the body, where the article explains how to find out your own
     number. Descriptive anchor text, e.g. "SwimScore Advanced measures DNA
     fragmentation at home". Never "buy now" or "click here".
  2. Closing line 1.
- You may mention the next tier up once in plain text, without a link.

### Other links

- At least 2 links to related live SwimScore articles in the body. Only link to
  handles confirmed live in step 1.
- `/pages/for-clinics` in closing line 2, worded as: "If you're a clinic looking
  to offer fertility testing to your patients, sign up here."

### SEO fields

Also produce an **SEO meta title** (~55-60 chars), an **SEO meta description**
(~150-160 chars), a **URL handle**, and a 1-2 sentence **summary**.

### Quality gate

Before finalizing, run [`CONTENT_CHECKLIST.md`](./CONTENT_CHECKLIST.md) end to
end and fix anything that fails.

---

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
   - `blogId`: News blog id above. `author: { name: "Denys Vasylenko" }`.
   - `body`: the HTML. `summary`: the teaser HTML. `handle`: the SEO handle.
   - `tags`: relevant topic tags.
   - `image`: `{ url: <resourceUrl>, altText: <descriptive, relevant alt text> }`.
   - **Metafields**:
     - `{ namespace: "global", key: "title_tag", type: "single_line_text_field", value: <meta title> }`
     - `{ namespace: "global", key: "description_tag", type: "single_line_text_field", value: <meta description> }`
     - `{ namespace: "swimscore", key: "draft_notes", type: "single_line_text_field", value: <category and reason, from Part 1 step 4> }`
   - **Draft + schedule**: create with `isPublished: false` (a hidden draft for
     review) and `publishDate` set to the intended posting time (ISO 8601 UTC).
     **Gotcha:** `articleUpdate` re-evaluates the publish state, so if you later
     edit the article you MUST pass `isPublished: false` again or Shopify can
     flip the draft live (or schedule it) when a `publishDate` is present. Always
     read back `isPublished` and confirm it is `false`.
     Default policy: leave as a hidden draft and only arm auto-publish after the
     content has been reviewed, unless the user has authorized auto-publish.
3. **Verify** by reading back `id, handle, isPublished, publishedAt, image.url,
   metafields` (including `swimscore.draft_notes`). The image URL should be on
   `cdn.shopify.com`.

## 7. Scheduling / the routine

A Claude routine (scheduled trigger) runs this whole workflow on a cadence. Each
run: discover existing articles, choose a topic per Part 1, research and write
per Part 2 and Part 3, generate a compliant hero image, and create the Shopify
draft with SEO and draft notes set and a `publishDate` on the desired posting
slot. Recommended posting slot: a weekday morning US Eastern, with a buffer
between draft creation and the publish date for review.

---

## Quick reference

| Item | Value |
| --- | --- |
| Store | SwimScore, `www.myswimscore.com` |
| News blog id | `gid://shopify/Blog/92195225782` (handle `news`) |
| Topic categories | A Cost, B Testing, C Meds/supplements/substances, D Result numbers, E Symptoms/conditions, F Life events, G Myths, H Lifestyle/environment |
| Variety rule | Not the same category as either of the last 2 articles |
| Draft notes | metafield `swimscore.draft_notes`: category + why picked |
| Product tier | Hormones -> Complete; DNA damage -> Advanced; else Essential |
| Product links | Exactly 2, both to the chosen tier (body + closing line 1) |
| Clinic page | `/pages/for-clinics` (closing line 2, "sign up here") |
| Hero image size | 1456 x 816, optimized JPG |
| Image people rule | Men, or man + woman couple. Never same-sex or women-only. |
| SEO meta title | metafield `global.title_tag` (~55-60 chars) |
| SEO meta description | metafield `global.description_tag` (~150-160 chars) |
| Hard writing rule | No em-dashes or en-dashes, ever |
| Every article ends with | italic CLIA / WHO 6th Edition line |
