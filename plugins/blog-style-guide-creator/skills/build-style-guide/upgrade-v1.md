# Upgrading a version 1 guide

A version 1 guide has numbered sections (`## 1. Voice and Tone`) and numbered rules (`### 1.2 ...`). The checks already read it as is; the upgrade gives every rule a stable ID, a severity, a scope, and a code check where one fits, while keeping the wording.

1. Run `sgc guide index-v1 <guide> --out <build>/v1-rules.json`. Each rule comes out as `V1-<number>` with a kind inferred from its section and `must` severity where the text says "always", "never", or "no exceptions".
2. When `sources/articles/` holds articles, run `sgc profile <brand_dir>/sources/articles --out <build>/profile.json`, so check parameters rest on counts.
3. Launch `blog-style-guide-creator:guide-builder` with `model: "${user_config.deep_model}"`, giving `<build>/v1-rules.json` as the only candidate file, the profile when there is one, the output `<build>/proposal.json`, and this instruction: upgrade a version 1 guide; keep each rule's wording; give each rule an area ID in place of its `V1-` number; add a lint check wherever the rule text states what one tests, with parameters from the text; set `source: doc`; leave out the old quick-reference section, since the checklist is generated; take `content_types` from the guide's text, or ask through the skill when it names none.
4. Render to `<build>/style-guide.proposed.md` without `--existing` and validate it. Show the user a table of old number, new ID, title, severity, and check, plus any v1 rule the proposal merged or dropped and why. Ask for approval as in step 5 of the skill.
5. On approval, write the version 1 text to `style-guide.v1.md` in the brand folder (the `v1_guide_backup` path `sgc brand-path` printed), then render the proposal to the guide path, run `sgc guide checklist` and `sgc guide validate`, and launch the guide auditor as in step 6 of the skill.

When the brand folder still has version 1's `articles/original/` and `articles/edited/` folders, offer `--edits` afterwards: those pairs can teach rules the version 1 guide never stated.
