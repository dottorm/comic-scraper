import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

import datetime
import cv2
from scraper.Scraper import Scraper
from panel_extractor.PanelExtractor import PanelExtractor
from text_extractor.TextExtractor import OCR
from utils import get_dates_list, create_dir
import numpy as np

full_images = "data/full-images"
splitted_images = "data/splitted-images"

if __name__ == "__main__":
    # get comic urls
    start_date = datetime.datetime(2021, 1, 1, 0, 0)
    end_date = datetime.datetime(2021, 1, 2, 0, 0)
    dates = get_dates_list(start_date, end_date)
    date_strings = [str(date.strftime('%Y-%m-%d')) for date in dates]
    comic_urls = [f"http://dilbert.com/strip/{date_string}" for date_string in date_strings]

    scraper = Scraper()
    # get asset url from the main page
    urls = scraper.get_asset_urls_multithreaded(comic_urls)
    # determing output paths, scrape images and save them
    create_dir(full_images)
    full_images_directory = full_images
    full_images_paths = [f"{full_images_directory}/{date}.png" for date in date_strings]
    scraper.scrape_and_save_multithreaded(urls, full_images_paths, max_workers=5)

    # extract panels from each full illustration
    create_dir(splitted_images)
    splitted_images_directory = splitted_images
    panel_extractor = PanelExtractor()
    splitted_images_paths = panel_extractor.extract_and_save_panels(full_images_paths, splitted_images_directory)

    # get transcriptions
    ocr = OCR("tesseract")
    transcriptions = ocr.extract_text(splitted_images_paths, clustering=True)

    # visualize
    for path in splitted_images_paths:
        image = cv2.imread(path) 
        words = transcriptions[path][0]
        bbox = transcriptions[path][1]
        wds = words.split(" ")
        for box in bbox:
            x1, y1, x2, y2 = box
            cv2.rectangle(image,(x1,y1),(x2,y2),(255, 255, 255),cv2.FILLED)
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imageGrayBlur = cv2.GaussianBlur(imageGray,(5,5),0)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        imageGrayBlurDilate = cv2.erode(imageGrayBlur, kernel)
        th, im_th = cv2.threshold(imageGrayBlurDilate, 200, 255, cv2.THRESH_BINARY_INV)
        hh, ww = im_th.shape[:2]
        mask = np.zeros((hh+2, ww+2), np.uint8)
        for box in bbox:
            x1, y1, x2, y2 = box
            cv2.floodFill(im_th, mask, (x1,y1), 128);
            im_th = cv2.bitwise_not(im_th)
            #fullfilled_balloons = im_th | im_floodfill_inv
        cv2.imshow("image", im_th)
        cv2.waitKey(0)
