from requestium import Session, Keys
from bs4 import BeautifulSoup as soup
from threading import Thread
import time


def read_from_txt(path):
    '''
    (str) -> list of str
    Loads up all sites from the sites.txt file in the root directory.
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
        print ("Couldn't locate <" + path + ">.")

    # Parse the data
    for line in raw_lines:
        lines.append(line.strip("\n"))

    # Return the data
    return lines


def get_images(endpoint):
    # Set up Selenium session
    s = Session(webdriver_path="chromedriver.exe", browser="chrome")
    # GET page
    s.driver.get(endpoint)
    # Get HTML
    html = s.driver.page_source
    # Parse HTML
    page = soup(html, "html.parser")
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
    links = []
    for raw_link in raw_links:
        # Skip links we got that we don't want (not from the side navbar)
        try:
            links.append(raw_link.span["title"])  # read from title attribute
        except:
            continue

    # Display links
    for link in links:
        file = open("images.txt", "a") 
        file.write(endpoint + ",  " + bellpage + ", " + link + "\n")
        file.close()

    s.driver.close()
    s.driver.quit()

class Handler:
    def __init__(self, links):
        # Save links for this tab
        self.links = links

    def start(self):
        # Go one link at a time in this "tab"
        for link in self.links:
            # Get images from link
            get_images(link)


if(__name__ == "__main__"):
    # Test
    # link = "https://my2.siteimprove.com/Inspector/624660/Accessibility/Page?pageId=14503756889&impmd=6508FEDFC411F126AA9F07EE75D47280#/Criterion/1.1.1/Check/1"
    # get_data(data)

    # Read links
    data = read_from_txt("sites.txt")

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
