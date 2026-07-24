# koenbotermans.com

Personal site + notebook blog, built with [Quarto](https://quarto.org) and
deployed to GitHub Pages. Every post is a Jupyter notebook run locally on GPU,
with an accompanying *Open in Colab* link.

See **[SETUP.md](SETUP.md)** for installation, the publishing workflow, and DNS.

```
_quarto.yml              site + blog config (narrow PaperMod-style column)
theme.scss               PaperMod-flavored styling
index.qmd                home page = post listing
about.qmd                about page
posts/                   one folder per post, each an index.ipynb
  _metadata.yml          shared post defaults
.githooks/pre-commit     executes staged notebooks on your GPU + updates Colab badge
scripts/                 helper that keeps the Colab badge in sync
.github/workflows/       renders and deploys to gh-pages on push
CNAME                    custom domain, preserved across deploys
```
