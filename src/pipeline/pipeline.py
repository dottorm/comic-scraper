import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import datetime
import cv2
from scraper.Scraper import Scraper
from panel_extractor.PanelExtractor import PanelExtractor
from text_extractor.TextExtractor import OCR#, inpaint_text
from utils import get_dates_list, create_dir, check_img, resize_img
import numpy as np

full_images = "data/full"
splitted_images = "data/splitted-images"
no_text = "/Volumes/CHIAVILLA/dottorato/dataset2/dilbert"

if __name__ == "__main__":
    """
    # get comic urls
    start_date = datetime.datetime(2022, 10, 10, 0, 0)
    end_date = datetime.datetime(2023, 1, 4, 0, 0)
    dates = get_dates_list(start_date, end_date)
    date_strings = [str(date.strftime('%Y-%m-%d')) for date in dates]
    comic_urls = [f"http://dilbert.com/strip/{date_string}" for date_string in date_strings]
    print(comic_urls)
    scraper = Scraper()
    # get asset url from the main page
    urls = scraper.get_asset_urls_multithreaded(comic_urls)
    print(urls)
    # determing output paths, scrape images and save them
    create_dir(full_images)
    full_images_directory = full_images
    full_images_paths = [f"{full_images_directory}/{date}.png" for date in date_strings]
    scraper.scrape_and_save_multithreaded(urls, full_images_paths, max_workers=4)
    """
    # extract panels from each full illustration
    #full_images_paths = [os.path.join(full_images, file) for file in os.listdir(full_images)]
    #create_dir(splitted_images)
    #splitted_images_directory = splitted_images
    #panel_extractor = PanelExtractor()
    #splitted_images_paths = panel_extractor.extract_and_save_panels(full_images_paths, splitted_images_directory)
    
    # get transcriptions
    #ocr = OCR("tesseract")
    #transcriptions = ocr.extract_text(splitted_images_paths, clustering=True)

    #create_dir(no_text)
    # save and visualize
    #for path in splitted_images_paths:
    for path in [os.path.join(no_text, file) for file in os.listdir(no_text)]:
        #img = cv2.imread(path)
        #head, tail = os.path.split(path)
        #words = transcriptions[path][0]
        #bbox = transcriptions[path][1]
        #wds = words.split(" ")
        #img = inpaint_text(img)
        
        #cv2.imwrite(os.path.join(no_text, tail), img)
        #cv2.imshow("image", img)
        #cv2.waitKey(0)
        #check_img(path)
        resize_img(cv2, path, '/Volumes/CHIAVILLA/dottorato/resized/')
    