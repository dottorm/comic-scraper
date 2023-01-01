import cv2
from tqdm import tqdm

from text_extractor.OCRPreprocessor import rescale_for_ocr, binarize_for_ocr
from text_extractor.OCRPostprocessor import cluster, clear_text, autocorrect_text
from text_extractor.TesseractOCR import TesseractOCR
from text_extractor.VisionOCR import VisionOCR

class OCR:

    #tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    tesseract_path = r'/Users/marco/tesseract/tesseract'
    cloud_credentials = '../../credentials/credentials.json'

    def __init__(self, engine):
        if engine == "tesseract":
            self.extractor = TesseractOCR(self.tesseract_path)
        elif engine == "vision-api":
            self.extractor = VisionOCR(self.cloud_credentials)
        else:
            raise Exception("Invalid OCR engine: supported engines are ")


    def extract_text(self, img_paths, rescale=False, binarize=False, clustering=True, autocorrect=False):
        """
        Extracts text from images.
        :param img_paths: A list of paths to images for processing.
        :param rescale: Bool determining if re-scaling pre-processing step should be applied.
        :param binarize: Bool determining if binarization pre-processing step should be applied.
        :param clustering: Bool determining if clustering-based output ordering post-processing step should be applied.
        :param autocorrect: Bool determining if autocorrect post-processing step should be applied.
        :return: A dictionary mapping image paths to the extracted names.
        """

        result = {}
        for path in tqdm(img_paths):
            sub_result = []
            image = cv2.imread(path)

            if rescale:
                image = rescale_for_ocr(image, self.tesseract_path)

            if binarize:
                image = binarize_for_ocr(image)

            bboxes, words = self.extractor.extract_text(image)
            
            if clustering:
                text = cluster(words, bboxes, image, visualize=False)
            else:
                text = ' '.join(words)

            text = clear_text(text)

            if autocorrect:
                text = autocorrect_text(text)
            
            sub_result.append(text)
            sub_result.append(words)
            result[path] = sub_result

        return result

    def remove_text(self, image, words):
        return self.extractor.remove_text(image, words)
        