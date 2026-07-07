# SwimScore Content Final Checklist

Run this checklist against every article **before it is left as a draft**. If any
item fails, fix it before finalizing. This is the last quality gate. It exists to
make sure SwimScore content is trustworthy, honest, genuinely helpful, and
readable by any everyday man.

Do not just tick boxes. For each section, quote or point to the specific
sentences that pass or fail, and fix what fails.

---

## 1. Are we pushing meds or supplements on people?

The article must **educate and inform a decision, never sell a drug or supplement.**

- [ ] The article does not tell the reader to take a specific drug or supplement.
      It explains options and trade-offs so they can decide with a clinician.
- [ ] Every intervention is presented with its limits: what it does not do, and
      who it will not help.
- [ ] Prescription treatments are clearly framed as clinician-managed and
      monitored, not self-administered.
- [ ] There is a genuine "what we are more skeptical about" beat, not just praise.
- [ ] The only call to action is to know your numbers / get tested / talk to a
      clinician (SwimScore's own product). Never "go buy" or "go take" a drug or
      supplement.
- [ ] No supplement-brand language: no "boost", "supercharge", "game changer",
      "optimize your potential".
- [ ] The tone would read as fair to a skeptical reader, a clinician, and a
      regulator. It could not reasonably be described as drug promotion.

## 2. Are we saying things that are not true?

Every factual claim must be traceable to a real source that actually says it.

- [ ] Every statistic, effect size, sample size, and threshold traces to a
      specific named study you actually read (Author et al., Journal, Year).
- [ ] The numbers match the source. No rounding or paraphrase that changes the
      meaning or oversells the effect.
- [ ] Each claim matches the study's real scope. Do not attribute a drug-class
      meta-analysis to a single drug. Do not present a surrogate-endpoint result
      (hormones, sperm parameters) as proof of pregnancy or live birth.
- [ ] Regulatory status is stated accurately (FDA-approved vs off-label vs
      compounded).
- [ ] Any claim the research flagged as thin, contested, or unverified is either
      cut or clearly labeled as uncertain. No repeating marketing numbers you
      could not verify in a primary source.
- [ ] Nothing is overstated beyond what the evidence shows. Where the evidence is
      mixed, the article says so.

## 3. Are we being helpful to people navigating the mixed research and online noise?

SwimScore is a beacon in a messy, over-marketed field.

- [ ] The article names the confusion or marketing the reader has likely run into
      and addresses it head-on.
- [ ] It clearly separates what is proven, what is uncertain, and what SwimScore
      recommends practically (the three-part frame).
- [ ] It gives a concrete, actionable path: know your numbers, the relevant
      thresholds, at least 12 weeks for any intervention, retest, and involve a
      clinician where it matters.
- [ ] A reader finishes better able to make a decision than a typical top Google
      result or a telehealth sales page would leave them.

## 4. Is it simple enough for every day males (laymans terms)?

- [ ] Every mechanism and clinical term is explained in plain English in the same
      breath it is introduced. No assumed biology (Sertoli cells, HPG axis,
      intratesticular, secondary hypogonadism, estradiol, etc. all get a plain
      gloss).
- [ ] Uses concrete analogies and short sentences.
- [ ] No paragraph could sit unchanged in a medical textbook.
- [ ] A smart man with no medical background could follow every paragraph.

## 5. Is this structured so an AI assistant can find and cite it?

SwimScore's goal is to be the source an AI assistant (ChatGPT, Claude, Perplexity, Google AI Overviews) lifts a clean answer from and attributes to us. See the skill's "Writing for AI and LLM Discoverability" section.

- [ ] Section headers are phrased as the natural question a reader would ask an AI assistant, where the section is answering one.
- [ ] Each section opens with a direct 1-2 sentence answer before getting into mechanism or nuance.
- [ ] Each section is self-contained. No "as mentioned above" or a dangling "it" that only resolves with the previous paragraph.
- [ ] Sentences that state a citable fact (CLIA certification, WHO thresholds, what the panel measures, a key study finding) name "SwimScore" explicitly rather than relying only on "we."
- [ ] Every number has its citation in the same sentence or the next one, not paragraphs later.
- [ ] Deep-dive and clinical explainer articles close with a 3-5 question Q&A block (Common Questions) after Our Take and before the italic closing lines. It restates the article's facts and introduces no new claims. Lifestyle pieces include one where the topic has a few clearly quotable facts.
- [ ] Terminology is consistent with the rest of the site ("SwimScore Complete," "WHO 6th Edition," "CLIA-certified," "DNA Fragmentation Index (DFI)"), not varied for style.

---

## Hard rules (also verify)

- [ ] **Zero em-dashes and zero en-dashes** anywhere. Scan explicitly.
- [ ] Internal links to relevant published SwimScore articles.
- [ ] A client CTA (`/products/swimscore-complete`) and, where natural, a clinic
      CTA (`/pages/for-clinics`).
- [ ] Closes with the italic CLIA / WHO 6th Edition line, plus a
      not-medical-advice line for clinical topics.
- [ ] Hero image follows the image rules (men only, or a man with a woman;
      relatable and realistic, not a fashion model; no text/AI artifacts).
- [ ] SEO meta title (~55-60 chars) and meta description (~150-160 chars) set.

## Publishing gotcha

- [ ] The article is left as a **hidden draft**: `isPublished: false`. When using
      `articleUpdate`, **always pass `isPublished: false` explicitly**, because
      Shopify re-evaluates the publish state on update and can flip a draft live
      (or schedule it) if a `publishDate` is present. Verify `isPublished` reads
      back as `false` after any update.
