from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.options import Options

from adblockparser import AdblockRules
import json
import os
import time

MIN_SIZE = 1024 # MIN image size in bytes
EASY_LIST = 'easylist.txt'
WEBLIST = 'weblist.json'
CHROME_DRIVER = './chromedriver'
# CHROME_BINARY = '../chromium/src/out/Default/chrome'

def create_adblock_filter():
    with open(EASY_LIST) as infile:
        return AdblockRules(list(map(lambda x: x.strip(), infile.readlines())))
        


def initialize_browser():
    # Create a new instance of the Chrome driver
    options = Options()
    # options.binary_location = CHROME_BINARY 
    # options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('window-size=1920,1080')
    options.add_argument('--enable-javascript')

    driver = webdriver.Chrome(chrome_options=options, executable_path=CHROME_DRIVER) 
    driver.set_window_size(1920,2000)
    return driver


def training_persona(driver):
    weblist = None
    with open(WEBLIST, 'r') as infile:
        weblist = json.load(infile)
    
    counter = 0
    for web in weblist:
        print("visiting {}".format(web))
        driver.get(web)
        counter+=1
        time.sleep(4)
        driver.save_screenshot('train/{}.png'.format(counter))

def collect_ads(driver, adblock_filter):
    counter = 1
    weblist = None
    with open(TEST_LIST, 'r') as infile:
        weblist = json.load(infile)
    weblist = ['https://www.nbcnews.com/']
    for web in weblist:
        driver.get(web)
        time.sleep(2)
        last_height = driver.execute_script("return window.scrollY")
        print("start_height {}".format(last_height))
        driver.save_screenshot('ads/screenshot_{}.png'.format(counter))
        max_scroll = 0
        while True:
            body = driver.find_element_by_css_selector('body')
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            new_height = driver.execute_script("return window.scrollY")
            print("new_height --> {}".format(new_height))
            print("last_height --> {}".format(last_height))
            if last_height == new_height or max_scroll==5:
                print('break')
                break
            counter += 1
            max_scroll += 1
            driver.save_screenshot('ads/screenshot_{}.png'.format(counter))
            last_height = new_height
            # scroll_height = height_adjust*1920
            # new_height = driver.execute_script("window.scrollTo(0, {})".format(str(scroll_height)))
            # height_adjust += 1
            # counter +=1
            # if new_height == last_height:
            #     break
            # driver.save_screenshot('ads/screenshot_{}.png'.format(counter))
            # last_height = new_height
            # time.sleep(2)


    # Access requests via the `requests` attribute
    # content_list = set()
    # ext_list = list()
    # counter = 0
    # for request in driver.requests:
    #     try:
    #         if request.response and request.response.headers['Content-Type']: # if its a valid url and has some content type
    #             if adblock_filter.should_block(request.url):
    #                 content_type = request.response.headers['Content-Type']
    #                 content_list.add(content_type)

    #                 if 'image' in content_type: # if there is an image in content type. save it
    #                     counter += 1 # change the counter so all file names are unique
    #                     ext_list.append(content_type.split(';')[0].split('+')[0].split('/')[1])
    #                     ext = ext_list[-1]
    #                     # write down this image
    #                     file_path = 'ads/{}'.format(str(counter)+'.'+ext)
    #                     print(request.url, content_type)
    #                     print("writing file {}".format(file_path))
    #                     with open(file_path, 'wb') as outfile:
    #                         outfile.write(request.response.body)
    #                     size = os.path.getsize(file_path)  #file size in bytes
    #                     print("size of img: {}".format(size))
    #                     if size < MIN_SIZE: #if size is less than 1kb then this is prolly an invalid img 
    #                         os.remove(file_path)
    #                         counter -= 1
                        
    #                     # try:
    #                     #     with open(file_path, 'r') as infile:
    #                     #         if infile.height * infile.width < MIN_SIZE:
    #                     #             os.remove(file_path)    
    #                     # except:
    #                     #     if ext != 'svg':
    #                     #         os.remove(file_path)

    #                 # check if this is an ad image
    #                 # if this is an ad img save it
    #                 # else continue

    #     except Exception as e:
    #         print(e)

    # for item in content_list:
    #     if 'image' in item:
    #         print(item)

    # for item in set(ext_list):
    #     print(item)
        



def main():
    driver = initialize_browser()
    # adblock_filter = create_adblock_filter()
    training_persona(driver)
    collect_ads(driver, adblock_filter)
if __name__ == '__main__':
    main()
