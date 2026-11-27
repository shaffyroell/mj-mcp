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

SwimScore's goal is to be the source an AI assistant (ChatGPT, Claude, Perplexity, Google AI Overviews) lifts a clean answer from and attributes to us. See the skill's "Writing to Be Cited" and "Bylines, Reviewer, and Attribution" sections.

- [ ] A three-sentence Key Takeaways block sits directly under the title. Each sentence is self-contained, specific, and quotable on its own.
- [ ] Section headers are phrased as the natural question a reader would ask an AI assistant, where the section is answering one.
- [ ] Each section opens with a direct 1-2 sentence answer before getting into mechanism or nuance.
- [ ] Each section and each key claim is self-contained. No "as mentioned above" or a dangling "it" that only resolves with the previous paragraph.
- [ ] Sentences that state a citable fact (CLIA certification, WHO thresholds, what the panel measures, a key study finding) name "SwimScore" explicitly rather than relying only on "we."
- [ ] Every claim cites a named source with a resolvable PubMed or DOI link, inline, not a vague tag like "(PMC, 2024)." Every statistic states its population in the same sentence.
- [ ] The article closes with a 3-5 question FAQ, phrased the way people actually search, after Our Take and before the italic closing lines. It restates the article's facts and introduces no new claims. Required for every content type.
- [ ] Research deep-dives and clinical explainers also close with a numbered References section listing every source cited, each with a link, placed after the FAQ and before the italic closing lines.
- [ ] The article has a named author and a "Medically reviewed by" line.
- [ ] Terminology is consistent with the rest of the site ("SwimScore Complete," "WHO 6th Edition," "CLIA-certified," "DNA Fragmentation Index (DFI)"), not varied for style.

---

## Hard rules (also verify)

- [ ] **Zero em-dashes and zero en-dashes** anywhere. Scan explicitly.
- [ ] Topic is in a category (A-H) different from both of the last 2 articles,
      and no live article already answers the same question.
- [ ] Title is the reader's question in their own words, and does not reuse
      "What the Research Actually Shows" if the newest live article uses it.
- [ ] Key Takeaways is exactly three sentences.
- [ ] A section titled "What we are more skeptical about" is present.
- [ ] Myth article (G): verdict in the first paragraph. Symptom article (E):
      says when to see a doctor promptly, and never says testing replaces an exam.
- [ ] Any supplement discussion states the Henriksen 2025 finding.
- [ ] Every price was checked live this run, with "Prices checked [Month Year]".
      Any DNA fragmentation price comparison uses only SwimScore Advanced and
      Legacy, both checked live this run; otherwise it is left out.
- [ ] Product tier chosen by the first matching rule (hormones -> Complete;
      DNA damage -> Advanced; else Essential), with **exactly two** product
      links, both to that tier (one in the body with descriptive anchor text,
      one in closing line 1).
- [ ] At least 2 body links to related live SwimScore articles.
- [ ] Closing lines in italics, in order: (1) "Want to know your own numbers?"
      tier line, (2) "If you're a clinic looking to offer fertility testing to
      your patients, sign up here." linking `/pages/for-clinics`, (3) "Related
      reading:" with 1-2 live articles, (4) not-medical-advice line, (5) CLIA /
      WHO 6th Edition line.
- [ ] Draft notes (category + why picked) saved in metafield
      `swimscore.draft_notes`, not in the article.
- [ ] Hero image follows the image rules (men only, or a man with a woman;
      relatable and realistic, not a fashion model; no text/AI artifacts).
- [ ] SEO meta title (~55-60 chars) and meta description (~150-160 chars) set.

## Publishing gotcha

- [ ] The article is left as a **hidden draft**: `isPublished: false`. When using
      `articleUpdate`, **always pass `isPublished: false` explicitly**, because
      Shopify re-evaluates the publish state on update and can flip a draft live
      (or schedule it) if a `publishDate` is present. Verify `isPublished` reads
      back as `false` after any update.
