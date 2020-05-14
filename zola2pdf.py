import pypandoc
import yaml
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

DIR = "../kompetenzwerkd.github.io/content"


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


def iter_files(path):
    """
    Returns the filepaths and their direcotiry depth of all 
    .md files in the directories and its subdirectories. 
    sorted by alphabet.
    """
    directories = defaultdict(list)
    for p in path.glob("./**/*.md"):
        directories[(str(p.parents[0]))].append(str(p))
    
    for folder, files in directories.items():
        depth = len(folder.split("/")) - 4
        for f in sorted(files):
            current_depth = depth
            if not f.endswith("_index.md"):
                current_depth += 1
            if depth < 0:
                current_depth = 0
            yield f, current_depth


def set_header_depth(text, depth):
    """
    Changes all headers of a markdown formated text based
    on the depth value. does this for "# " until "###### ".
    E.g. 
    depth=2:
    "# Title" -> "### Title"
    depth=1:
    "## Subtitle" -> "### Subtitle" 
    """
    for i in range(1, 6):
        header = r"[\n|^]({} )".format("#"* (6-i))
        new_header = "\n{} ".format("#"* (6-i + depth))
        #print(header, " -> ", new_header)
        #text = text.replace(header, new_header)
        text = re.sub(header, new_header, text)
    return text



if __name__ == "__main__":
    
    date = datetime.now().isoformat()
    out_file = "ebook/kompetenzwerkd_infoportal.pdf"
    out_file_archive = "ebook/archive/kompetenzwerkd_infoportal_{}.pdf".format(date[:10].replace("-", "_"))

    content = METADATA.format(date[:10])

    path = Path(DIR)

    for p, depth in iter_files(path):

        #skip impressum and ebook page
        if "impressum.md" in p or "ebook.md" in p:
            continue

        with open(p) as f:
            new = f.read()

            print("\t", p, depth)

            # change headers
            new = set_header_depth(new, depth)

            # remove metadata
            new = new.split("+++")[-1]

            #add new page if index.md
            if "_index.md" in p and (depth == 0):
                new = "\\pagebreak\\newpage \n\n"+new

            content += new

    # replace relative image paths with full paths
    content = content.replace("![](images", "![](/home/muehleder/code/kompetenzwerkd.github.io/static/images")

    # replace problematic unicode characters
    content = content.replace("➜", "->")
    content = content.replace("✪", "*")
    content = content.replace("➤", ">")

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