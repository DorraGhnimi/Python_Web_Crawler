from html.parser import HTMLParser
# generic html parser

from urllib import parse


# LinkFinder Class inhereting from HTMLParser
class LinkFinder(HTMLParser):
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url  # home page, nabdou baha
        self.page_url = page_url  # page actuelle
        self.links = set()

    # Called only on start tag of an html data
    # overwrite
    def handle_starttag(self, tag, attributes):
        if tag == 'a':
            for (attribute, value) in attributes:
                if attribute == 'href':
                    # bech ken relative yzid'ha lhome  sinon non .. 'join'
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass

# finder = LinkFinder()
# finder.feed('<html><head><title>test</title></head>'
#             '<body>test the start tag method</body></html>')
