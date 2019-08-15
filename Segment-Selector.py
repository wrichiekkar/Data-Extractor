from selenium import webdriver
from bs4 import BeautifulSoup as Soup
from threading import Thread
import time
import math
start = time.time()  # start timer
clist = [] #To count # of sites finished

def read_from_txt(path):
    '''
    (str) -> list of str
    Loads up all sites from the .txt file in the root directory.
    Returns the sites as a list
    '''
    #Initialize variables
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

def get_images(endpoint):
    # Set up Selenium session
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    #options.add_argument('window-size=1200x600')

    s = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

    # GET page
    s.get(endpoint)
    # Get HTML
    html = s.page_source
    # Parse HTML
    page = Soup(html, "html.parser")
    # Find all instances of (...)
    raw_links = page.findAll("div", {"class": "list-cell is-truncated is-fill"})
    # Click next page option
    try:
        while(page.find("button", {"title": "Next page "}) is not None and not page.find("button", {"title": "Next page "}).has_attr("disabled")): # find "next page" that is not disabled
            _id = page.find("button", {"title": "Next page "})["id"]  # Find ID for button
            s.find_element_by_id(_id).click()
            page = Soup(s.page_source,"html.parser")  # Get new page's HTML
            temp = page.findAll("div", {"class": "list-cell is-truncated is-fill"})
            for t in temp:  # store new data in old array
                raw_links.append(t)
    except Exception as e:
        print(e)

    # Get original page link
    bellpage = s.find_element_by_xpath('//*[@id="inspector"]/div[1]/div/div[2]/div[1]/div[1]/a/div/div/div').text
    # Parse the image links
    # links = []

    for raw_link in raw_links:
        # Skip links we got that we don't want (not from the side navbar)
        try:
            link = raw_link.span.text # read from span tag
            # links.append(raw_link.span["title"])  # read from title attribute
        except:
            continue
    # Display links
        file = open("Btext.txt", "a")
        file.write(endpoint + "," + bellpage + "," + link + "\n")
        file.close()

    s.close()

class Handler:
    def __init__(self, links):
        # Save links for this tab
        self.links = links

    def start(self):
        # Go one link at a time in this "tab"
        for link in self.links:
            # Get images from link
            get_images(link)
            count = 1  # start counter and timer
            clist.append(count)
            total = sum(clist)
            end = time.time()
            minute = int(math.floor(end-start)/60)
            sec = math.floor((end-start)%60)
            print(total, minute, + sec)

if(__name__ == "__main__"):
    # Read links
    data = read_from_txt("Sites.txt")
    # Test
    # data = 'https://my2.siteimprove.com/Inspector/624660/Accessibility/Page?pageId=14507558020&impmd=6508FEDFC411F126AA9F07EE75D47280#/Criterion/1.3.1/Check/30'
    # get_images(data)

    # Calculate how many links each handler should process
    handler_size = len(data)//5  # 5 tabs
    # Split up links for 10 tabs [inclusive,exclusive]
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


