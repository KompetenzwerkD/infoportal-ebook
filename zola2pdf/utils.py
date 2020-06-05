import toml
import re

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

def load_zola_md(filepath):
    """
    Loads a zola markdown file and returns its metadata (as dict) and 
    content as string
    """

    meta = {}
    text = {}

    with open(filepath) as f:
        md = f.read()

    split = md.split("+++")
    if len(split) != 3:
        print("invalid zola markdown file")
        raise IOError
    text = split[-1]
    meta = toml.loads(split[1])

    return meta, text


def remove_html(s):
    r = re.compile('<.*?>')
    clean = re.sub(r, '', s)
    return clean