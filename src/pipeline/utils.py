import os
import datetime
from PIL import Image

def get_dates_list(start_date, end_date):
    """
    Produces a list of dates between the given boundaries.
    :param start_date: Starting date for the date range.
    :param end_date: Ending date for the date range.
    :return: A list of dates.
    """
    return [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days)]


def create_dir(dir_name):
    if(not os.path.exists(dir_name)):
        os.makedirs(dir_name)

def check_img(path):
    i = 0
    if path.endswith('.png'):
            try:
                img = Image.open(path)  # open the image file
                img.verify()  # verify that it is, in fact an image
            except (IOError, SyntaxError) as e:
                print(path)
                #os.remove(path)
                i = i+1
    
    return i

def resize_img(cv2, path, output_path):

    create_dir(output_path)

    img = cv2.imread(path)

    file_name = os.path.basename(path)

    # Get original height and width
    print(f"Original Dimensions : {img.shape}")

    # resize image by specifying custom width and height
    resized = cv2.resize(img, (512, 512))

    output = output_path + file_name

    print(f"Resized Dimensions : {resized.shape}")
    cv2.imwrite(output, resized)