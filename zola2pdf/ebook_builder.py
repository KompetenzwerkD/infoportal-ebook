
class EbookBuilder():
    """
    Iterates through a Section object representing a zola
    webpage content direcotry and builds a single markdown
    text string from it.
    """


    def _filter_pages(self, section):
        for p in section.pages:
            skip = False
            for token in self.skip_pages:
                if str(p.filepath).endswith(token):
                    skip = True
                    break
            if not skip:
                yield p

    def _load_section_content(self, section):

        if section.depth == 0:
            self.text += "\\pagebreak\\newpage \n\n"

        self.text += section.index_page.text
        
        for p in self._filter_pages(section):
            print("\t"*p.depth + p.meta["title"])
            self.text += p.text

        for s in section.sections:
            print("\t"*s.depth + s.index_page.meta["title"])
            self._load_section_content(s)


    def __init__(self, content_section, front_matter="", skip_pages=None):
        self.content = content_section

        self.text = front_matter

        if skip_pages:
            self.skip_pages = skip_pages
        else:
            self.skip_pages = []

        self._load_section_content(self.content)