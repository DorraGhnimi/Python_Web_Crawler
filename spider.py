from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Spider:
    # Class variables (static in java) , to be shared among all instances (spiders)
    project_name = ''
    base_url = ''  # home page, start from here
    domain_name = ''
    # Actual file, stored in Disk, save data if we shut the computer down
    queue_file = ''
    crawled_file = ''
    # Coz files are not efficient at all, specially when w're working with Multithreading w kadha
    # Variable, set, stored in  RAM, to be quick, coz working only with file will slow the program down
    queue_set = set()
    crawled_set = set()

    def __init__(self, project_name, base_url, domain_name):
        # to be shared between all spieders (coz static)
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name

        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'

        # create the directory, and queue and crawle files
        self.boot()
        # first spider, crawl home page and gather some link, then we will create some other spiders to help him out
        self.crawl_page('first_spider', Spider.base_url)

    @staticmethod
    def boot():
        # 1 our project
        create_project_dir(Spider.project_name)
        # 2 our queue and crawled files
        create_data_files(Spider.project_name, Spider.base_url)
        # 3 and then we convert em to sets w netwaklou
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled_set:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue_set)) + ' | crawled ' + str(len(Spider.crawled_file)))
            # gather links from page_url and add them to the queue_set (to be crawled later)
            Spider.add_links_to_queue(Spider.gather_link(page_url))
            # update sets, after crawling  page_url (the actual page)
            Spider.queue_set.remove(page_url)
            Spider.crawled_set.add(page_url)
            # update files
            Spider.update_files()

    @staticmethod
    def gather_link(page_url):
        html_string = ''
        try:
            # connect
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)

        except:
            print('Error: can not crawl page')
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue_set:
                continue
            if url in Spider.crawled_set:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue_set.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue_set, Spider.queue_file)
        set_to_file(Spider.crawled_set, Spider.crawled_file)

