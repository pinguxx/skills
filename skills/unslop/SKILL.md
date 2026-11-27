---
name: unslop
description: Cut AI tells from any writing. Use when drafting, editing, or reviewing READMEs, documentation, release notes, blog posts, launch copy, or comments to strip AI writing patterns while preserving meaning and tone.
---

# Unslop

Edit text to remove AI patterns. Scan for the patterns below, then rewrite. Preserve meaning and match the intended tone.

Rule numbers are stable ids that other skills cite. A removed rule leaves a gap.

1. No trailing "-ing" phrases that add no fact ("highlighting...", "ensuring...").
2. No vague attributions ("experts believe"). Name the source or delete.
3. No AI vocabulary: additionally, crucial, delve, enhance, foster, landscape, pivotal, showcase, testament, underscore, vibrant.
4. Say "is" or "has", not "serves as", "stands as", "boasts", "features".
5. No "not just X, but Y". State the point.
6. Don't force ideas into threes.
7. One name per thing. Repeat it.
8. No "from X to Y" unless X and Y sit on a real scale.
9. No em dashes, en dashes, or hyphens used as dashes, and no parentheses in their place. Use a period or a comma.
10. A colon goes before a list or an example, never mid-sentence as a connector.
11. Don't bold every proper noun or acronym.
12. No bold label and colon that restates its line ("Performance: Performance improved..."). A bold lead-in that ends in a period and adds new detail is fine.
13. Sentence case headings.
14. No decorative emojis.
15. Straight quotes.
16. No chatbot phrases ("I hope this helps!", "Let me know if...").
17. No praise or agreement openers. Respond directly.
18. Cut filler. "In order to" becomes "to". Delete "it is important to note that".
19. One hedge at most: "may".
20. No generic conclusions. State specific plans or facts.
21. No abstract metaphor nouns: substrate, wedge, vector, nexus, primitive, harness, surface, scaffolding, paradigm, ratchet, north star, flywheel. Use the concrete word.
22. Say what it does, not how it feels. Name the mechanism or the number.
23. Cut a sentence that could appear unchanged in another project's docs.
24. One idea per sentence. Split a sentence the reader has to reread.
25. Active voice. Name the actor unless it is unknown or doesn't matter.
26. Cut adverbs or use a stronger verb.
27. Give the number.
28. Use the plain word: "use", not "utilize" or "leverage".
29. No metaphor, aphorism, personified code, or figurative verb where a literal phrase exists.
30. Write whole sentences with their articles and verbs. Spell out arrows and abbreviations.

## Automated mechanical scan

Run the bundled zero-dependency scanner first to catch mechanical violations (rules 3, 4, 5, 9, 15, 18, 21, 28) while skipping code blocks and URLs:

```bash
python3 scripts/check_unslop.py <file1.md> [file2.md ...]
```

Fix every reported finding, then do a manual pass for the remaining judgment-based rules.
