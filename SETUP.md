# Setup

A Quarto website where every post is a Jupyter notebook. You run notebooks
locally on your GPU; a pre-commit hook executes them and refreshes their
Colab badge; GitHub Actions renders and deploys to GitHub Pages (free) at
`koenbotermans.com`.

---

## 1. One-time local setup

```bash
# Install Quarto (macOS)
brew install quarto           # or download from https://quarto.org/docs/get-started/

# From the repo root, activate the pre-commit hook (versioned in .githooks/)
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit

# You need Jupyter + nbconvert in the env that has your GPU kernel
pip install jupyter nbconvert
```

Preview the site locally at any time:

```bash
quarto preview        # live-reloading local server
```

## 2. Create the GitHub repo

```bash
git init
git add .
git commit -m "Initial site"                       # hook runs on the example notebook
git branch -M main
git remote add origin git@github.com:JPABotermans/website.git
git push -u origin main
```

The push triggers `.github/workflows/publish.yml`, which renders the site and
pushes it to a `gh-pages` branch.

## 3. Turn on GitHub Pages

Repo → **Settings → Pages**:

- **Source:** Deploy from a branch
- **Branch:** `gh-pages` / `root`
- **Custom domain:** `koenbotermans.com` → Save
- Tick **Enforce HTTPS** once the certificate is issued (after DNS resolves)

The `CNAME` file in this repo keeps the custom domain across deploys.

## 4. Point the domain at GitHub (in GoDaddy)

GoDaddy is only your **registrar** here — it holds the name and forwards it.
Hosting stays free on GitHub Pages. In GoDaddy → **Domain → DNS → Manage DNS**,
set these records:

| Type  | Name | Value               |
|-------|------|---------------------|
| A     | @    | 185.199.108.153     |
| A     | @    | 185.199.109.153     |
| A     | @    | 185.199.110.153     |
| A     | @    | 185.199.111.153     |
| CNAME | www  | JPABotermans.github.io |

Optional IPv6 (add alongside the A records, don't replace them):

| Type | Name | Value                  |
|------|------|------------------------|
| AAAA | @    | 2606:50c0:8000::153    |
| AAAA | @    | 2606:50c0:8001::153    |
| AAAA | @    | 2606:50c0:8002::153    |
| AAAA | @    | 2606:50c0:8003::153    |

Delete any GoDaddy "Parked" A record on `@` first. DNS can take minutes to a few
hours. Verify with `dig koenbotermans.com +short` (should return the four IPs).

---

## Writing a new post

```bash
mkdir posts/my-new-post
# put your notebook at posts/my-new-post/index.ipynb
```

The notebook's first cell is a **raw** cell holding the front matter:

```
---
title: "My New Post"
description: "One-line summary shown on the home page."
date: "2026-07-25"
categories: [robotics]
---
```

Then just write and run cells normally in Jupyter/VS Code on your GPU. When you
commit:

1. the pre-commit hook inserts/updates the **Open in Colab** badge (pointed at
   this notebook's path in the repo),
2. re-executes the notebook so the committed outputs are fresh,
3. re-stages it.

Push, and the site rebuilds and redeploys automatically.

### Bypassing the hook

- Slow notebook you don't want to re-run right now: `SKIP_NB_EXEC=1 git commit ...`
- Skip all hooks: `git commit --no-verify ...`

---

## How it fits together

```
you (GPU) ──run notebook──► outputs saved in index.ipynb
   │
   └─ git commit ─► pre-commit: badge + execute + restage
                     │
                     └─ git push ─► GitHub Actions: quarto render ─► gh-pages
                                       │
                                       └─ GitHub Pages serves koenbotermans.com
```

CI never runs Python — it only renders the saved outputs, so builds are fast and
never need your data or a GPU. All execution stays on your machine.

## Notes on Colab

The badge points at `.../github/JPABotermans/website/blob/main/posts/<slug>/index.ipynb`.
Colab opens whatever is in the repo. If a notebook depends on local paths, private
datasets, or a specific CUDA setup, it may need small tweaks (e.g. a `pip install`
cell or a data-download cell) to run unmodified in Colab.
