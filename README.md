# Infoportal E-book

Create a pdf-ebook from the contents of the KompetenzwerkD-Infoportal.

## Requirements

- Python 3.8
- Pandoc 
- Latex (with German language package)

- [A clone of the KompetenzwerkD website repository](https://www.github.com/kompetenzwerkd/infoportal)

## Use

```źsh
$ python build_ebook.py
```

Builds a new ebook version of the website, overwrites the current one (`ebook/kompetenzwerkd_infoportal.pdf`) and places a copy with a timestamp  in the archive (`ebook/archive/kompetenzwerkd_infoportal_<DATE>.pdf`).

Configuraiton (website content diretory, the pdf title page, etc.) is at the moment directly defined in `build_ebook.py`.

## Lincense

MIT

## Authors

[kompetenzwerkd@saw-leipzig.de](kompetenzwerkd@saw-leipzig.de)