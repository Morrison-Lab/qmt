# Claude Code Instructions

Project guidance for Claude Code (CLI, IDE, and the GitHub Action). The same conventions apply to GitHub Copilot — see [`.github/copilot-instructions.md`](.github/copilot-instructions.md), which is the source of truth for style.

## Project context

`qmt` (Quarto Manuscript Template) is a template repository for
[Quarto manuscripts](https://quarto.org/docs/manuscripts/) maintained
by the UCD-SERG lab. Downstream repos are created from this template
via the GitHub "Use this template" button, so changes here propagate
to new manuscripts.

Authoritative style guide: [UCD-SERG Lab Manual](https://ucd-serg.github.io/lab-manual/) (source: <https://github.com/UCD-SERG/lab-manual>).

## Repository layout

- `index.qmd` — the main manuscript article
- `notebooks/` — supplementary Quarto notebooks embedded in the HTML output
- `_quarto.yml` — Quarto project configuration
- `_extensions/` — vendored Quarto extensions
- `R/`, `man/`, `DESCRIPTION`, `NAMESPACE` — the project is also a small R package
- `references.bib` — BibTeX bibliography
- `styles.css` — manuscript styling
- `.github/workflows/` — CI workflow definitions
- `.github/scripts/` — helper scripts used by workflows
- `_manuscript/`, `_freeze/`, `.quarto/` — build artifacts (do not edit by hand)

## Style conventions

Mirrors [`.github/copilot-instructions.md`](.github/copilot-instructions.md). Key points:

- **Lists of 3+ items**: use bullet lists rather than comma-separated prose. Always leave a blank line before a markdown bullet list (especially in `.qmd` files).
- **Code chunks**: HTML output folds code by default (the site config sets `code-fold: true` with `code-tools: true`, as rme does). Keep the default when the *output* (plot, table) is the point and the code is incidental. Set `#| code-fold: false` on tutorial code, short examples, code that is the main focus, or chunks where the console output is the main content.
- **R style**: respect `.lintr.R`. Run `lintr::lint_dir()` before declaring R changes done.
- **Quarto chunks**: prefer chunk options as YAML-style `#|` directives, not as inline `r, opt = val` arguments.

## Working in this repo

- **Don't edit generated files**: `README.md` is built from `README.Rmd`; `_manuscript/` and `_freeze/` are build outputs.
- **Local preview**: `quarto preview` (live reload). Full build: `quarto render`. When verifying a single edited file, render just that file (`quarto render index.qmd --to html`) rather than the whole project.
- **Spell check**: words go in `inst/WORDLIST` (see `.github/workflows/check-spelling.yaml`). Update the wordlist instead of disabling the check.
- **Link check**: tuned in `lychee.toml`; prefer fixing broken links over adding exceptions.

## ai-config plugin

`.claude/settings.json` declares the `Morrison-Lab` marketplace (source:
[`Morrison-Lab/ai-config`](https://github.com/Morrison-Lab/ai-config)) and enables
its `ai-config@Morrison-Lab` plugin, along with the `posit-dev-skills` and `sembr`
marketplaces this template also carries, matching
[`Morrison-Lab/qbt`](https://github.com/Morrison-Lab/qbt). Declaring is not
installing: a local session still needs `claude plugin install ai-config@Morrison-Lab`
once. Because this is a template repository, this declaration is copied once into
every repo created from it — an omission here silently ships to every downstream
manuscript.

## Pull request expectations

- Keep PRs scoped — bug fixes shouldn't smuggle in refactors.
- Write commit messages and PR descriptions explaining the *why*, not just the *what*.
- Don't bypass CI failures (spell check, link check, lint) — fix the underlying issue.
- Don't commit `_manuscript/` or `_freeze/` changes unless that is genuinely the intent of the PR.

## Things to avoid

- Adding new top-level dependencies (R packages, Quarto extensions) without a clear reason; this is a template, so every dependency lands in every downstream manuscript.
- Reformatting unrelated files.
- Inventing URLs or citations — only use sources actually present in `references.bib` or explicitly provided.
