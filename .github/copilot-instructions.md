# GitHub Copilot Instructions

Project guidance for GitHub Copilot. The same conventions apply to Claude Code — see [`CLAUDE.md`](../CLAUDE.md).

## Project context

`qmt` (Quarto Manuscript Template) is a template repository for
[Quarto manuscripts](https://quarto.org/docs/manuscripts/) maintained by the
UCD-SERG lab. Downstream repos are created from this template via the GitHub
"Use this template" button.

Authoritative style guide: [UCD-SERG Lab Manual](https://ucd-serg.github.io/lab-manual/).

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

- **Lists of 3+ items**: use bullet lists rather than comma-separated prose. Always leave a blank line before a markdown bullet list.
- **Code chunks**: HTML output folds code by default (the site config sets `code-fold: true` with `code-tools: true`, as rme does). Keep the default when the *output* is the point and the code is incidental; set `#| code-fold: false` on tutorial code, short examples, code that is the main focus, or chunks where the console output is the main content.
- **R style**: respect `.lintr.R`. Run `lintr::lint_dir()` before declaring R changes done.
- **Quarto chunks**: prefer chunk options as YAML-style `#|` directives, not as inline `r, opt = val` arguments.

## Working in this repo

- **Don't edit generated files**: `README.md` is built from `README.Rmd`; `_manuscript/` and `_freeze/` are build outputs.
- **Local preview**: `quarto preview` (live reload). Full build: `quarto render`.
- **Spell check**: words go in `inst/WORDLIST`. Update the wordlist instead of disabling the check.
- **Link check**: tuned in `lychee.toml`; prefer fixing broken links over adding exceptions.

## Things to avoid

- Adding new top-level dependencies (R packages, Quarto extensions) without a clear reason; this is a template, so every dependency lands in every downstream manuscript.
- Committing `_manuscript/`, `_freeze/`, or `.quarto/` build artifacts.
- Reformatting unrelated files.
- Inventing URLs or citations — only use sources actually present in `references.bib` or explicitly provided.
