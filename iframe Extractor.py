from selenium import webdriver
from bs4 import BeautifulSoup as Soup
from threading import Thread
import time
import math
start = time.time()  # start timer
clist = []  # To count # of sites finished


def read_from_txt(path):
    '''
    (str) -> list of str
    Loads up all sites from the .txt file in the root directory.
    Returns the sites as a list
    '''
    # Initialize variables
    raw_lines = []
    lines = []

    # Load data from the txt file
    try:
        f = open(path, "r")
        raw_lines = f.readlines()
        f.close()
    # Raise an error if the file couldn't be found
    except:
        print("Couldn't locate <" + path + ">.")

    # Parse the data
    for line in raw_lines:
        lines.append(line.strip("\n"))

    # Return the data
    return lines


def get_data(endpoint):
    # Set up Selenium session
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    #options.add_argument('window-size=1200x600')

    s = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

    # GET page
    s.get(endpoint)

    # Get original page link
    bellpage = s.find_element_by_xpath('//*[@id="inspector"]/div[1]/div/div[2]/div[1]/div[1]/a/div/div/div').text

    s.find_elements_by_class_name("button-inner")[4].click()  # Click HTML button

    iframes = Soup(s.page_source, "html.parser").find("div", {"class": "source-view-document"}).text  # Read HTML section
    iframes2 = Soup(iframes, "html.parser").findAll("iframe")  # Parse all iframes

    for iframe in iframes2:
        if(not iframe.has_attr("title") or iframe["title"].strip() == ""):  # print ones without title or empty title
            file = open("iframe.txt", "a")
            file.write(endpoint + "," + bellpage + "," + str(iframe) + "\n")
            file.close()

    s.quit()

class Handler:
    def __init__(self, links):
        # Save links for this tab
        self.links = links

    def start(self):
        # Go one link at a time in this "tab"
        for link in self.links:
            # Get images from link
            get_data(link)
            count = 1  # start counter and timer
            clist.append(count)
            total = sum(clist)
            end = time.time()
            minute = int(math.floor(end-start)/60)
            sec = math.floor((end-start)%60)
            print(total, minute, + sec)


if(__name__ == "__main__"):
    # Read links
    data = read_from_txt("iframe_sites.txt")
    # Test
    # data = 'https://my2.siteimprove.com/Inspector/624660/Accessibility/Page?pageId=23655236785&impmd=6508FEDFC411F126AA9F07EE75D47280#/Criterion/4.1.2/Check/13'
    # get_data(data)

    # Calculate how many links each handler should process
    handler_size = len(data)//5  # 5 tabs
    # Split up links for 5 tabs [inclusive,exclusive]
    handler1_links = data[0:handler_size]
    handler2_links = data[handler_size:(2*handler_size)]
    handler3_links = data[(2*handler_size):(3*handler_size)]
    handler4_links = data[(3*handler_size):(4*handler_size)]
    handler5_links = data[(4*handler_size):(5*handler_size)]

    # Create handler, basically 1 tab. Create tab.
    handler1 = Handler(handler1_links)
    handler2 = Handler(handler2_links)
    handler3 = Handler(handler3_links)
    handler4 = Handler(handler4_links)
    handler5 = Handler(handler5_links)

    # Start 5 handlers in parallel
    Thread(target=handler1.start).start()
    Thread(target=handler2.start).start()
    Thread(target=handler3.start).start()
    Thread(target=handler4.start).start()
    Thread(target=handler5.start).start()
