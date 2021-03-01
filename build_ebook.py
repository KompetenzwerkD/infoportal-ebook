import pypandoc
from datetime import datetime

from zola2pdf import Section, EbookBuilder

CONTENT_DIR = "../infoportal/content"

METADATA = """
---
title:  "KompetenzwerkD Infoportal"
subtitle: "[ Ebook-Version | Stand: {} ]"
author: 
    - "Franziska Naether"
    - "Dirk Goldhahn"
    - "Peter Mühleder"
---
"""

SKIP_PAGES = [
    "ebook.md",
    "impressum.md",
    "sonderzeichen.md"
]



if __name__ == "__main__":
    
    date = datetime.now().isoformat()

    out_file = "ebook/kompetenzwerkd_infoportal.pdf"
    out_file_archive = "ebook/archive/kompetenzwerkd_infoportal_{}.pdf".format(date[:10].replace("-", "_"))

    # load webpage content and build ebook markdown string
    page = Section(CONTENT_DIR, root=True)
    ebb = EbookBuilder(
        page,
        front_matter=METADATA.format(date[:10]),
        skip_pages=SKIP_PAGES
        )
    content = ebb.text

    # replace problematic unicode characters
    content = content.replace("➜", "->")
    content = content.replace("✪", "*")
    content = content.replace("➤", ">")
    content = content.replace("⚠", "[!]")
    content = content.replace("☆", "*")

    # convert to pdf
    pypandoc.convert_text(content, 
        'latex', 
        format="md", 
        extra_args=["--toc", "--number-sections", "--template=./template.tex", "-V", "lang:de"],
        outputfile=out_file)

    # craete archive version
    pypandoc.convert_text(content, 
        'latex', 
        format="md", 
        extra_args=["--toc", "--number-sections", "--template=./template.tex", "-V", "lang:de"],
        outputfile=out_file_archive)