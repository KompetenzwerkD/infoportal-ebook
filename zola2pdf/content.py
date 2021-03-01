from pathlib import Path
from .utils import load_zola_md, set_header_depth, remove_html

class Page():
    """
    class representing a zola content page
    """


    def __init__(self, filepath, depth):
        self.filepath = filepath
        self.base_path = Path(str(filepath).split("/content/")[0]).resolve()

        self.depth = depth

        meta, text = load_zola_md(filepath)
        self.meta = meta

        print(self.base_path)

        #replace static image links
        text = text.replace("![](images", "![]({}/static/images".format(self.base_path))
        text = text.replace("](infoportal/images", "]({}/static/images".format(self.base_path))
        text = text.replace("](/infoportal/images", "]({}/static/images".format(self.base_path))

        #replace remove html tags

        # change headers
        text = set_header_depth(text, depth)

        self.text = remove_html(text)



class Section():
    """
    class representing a zola content section
    """

    def __init__(self, directory, depth=0, root=False):
        self.directory = directory

        self.depth = 0

        self.index_page = None
        self.pages = []
        self.sections = []
        for f in Path(directory).iterdir():
            if str(f).endswith("_index.md"):
                self.index_page = Page(f, depth)

            elif f.is_file and str(f).endswith(".md"):
                self.pages.append(Page(f, depth + 1))

            elif f.is_dir:
                if root == True:
                    next_depth = depth 
                else:
                    next_depth = depth + 1
                self.sections.append(Section(f, next_depth))

        #sort pages and sections
        if "sort_by" in self.index_page.meta:
            sort_by = self.index_page.meta["sort_by"]
            self.sections = sorted(self.sections, key=lambda x: x.index_page.meta[sort_by])
            
            try: 
                self.pages = sorted(self.pages, key=lambda x: x.meta[sort_by])
            except:
                print("cannot sort pages in section <{}> by <{}>".format(
                    self.directory,
                    sort_by
                ))
        else:
            print("no <sort by> set for section <{}>".format(self.directory))