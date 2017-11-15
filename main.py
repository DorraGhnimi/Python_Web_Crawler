import threading
from spider import Spider
from queue import Queue
from domain import *
from general import *

# Constants (in python there is no constants, it's just a convention )
PROJECT_NAME = 'thenewboston'
HOME_PAGE = 'https://thenewboston.com/'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
#  DOMAIN_NAME = 'thenewboston'
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8

queue = Queue()
# First Spider : first we need to gather from the home page
Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME)


# now we ll create 8 spiders to crawl the rest


# Create worker threads (will die when main exists)
def create_workers():
    #   "  _  " , coz i don't really need that variable, just want to loop: convention
    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=work)  # function work
        # daemon : " dhaaaharli" thread that die when main exits
        # optional
        thread.daemon = True
        thread.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queue link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# check if there are items in the queue, if so, crawl em
def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    if len(queue_links) > 0:
        print(str(len(queue_links)) + 'links in the queue')
        create_jobs()


create_workers()
crawl()














































# end
