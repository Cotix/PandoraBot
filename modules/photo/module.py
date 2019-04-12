import io
import pytesseract
import cv2
import numpy as np
from PIL import Image
from pytesseract import TesseractError

from modules.telegram_module import TelegramModule, photo


def get_new(old):
    new = np.ones(old.shape, np.uint8)
    cv2.bitwise_not(new,new)
    return new


class Photo(TelegramModule):
    @photo
    def recv_photo(self):
        """
        Probeert tekst te herkennen in foto's. Bij lange teksten reageert de bot met de
        gevonden tekst. Bij teksten die overeenkomen met kill of puzzle codes wordt die
        ingevuld.
        """
        photo = self.update.message.photo[-1]
        image_bytes = self.bot.get_file(photo.file_id).download_as_bytearray()
        nparr = np.asarray(image_bytes, np.uint8)

        # Convert image to grayscale
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Smooth out image with a simple filter
        kernel = np.ones((3, 3), np.float32) / 9
        img_smooth = cv2.filter2D(img2gray, -1, kernel)

        # Adaptive threshold to filter out big consistent regions
        img_threshold = cv2.adaptiveThreshold(img_smooth, 255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV,
                                        13, 7)
        # erode small noise away
        new_img = cv2.erode(img_threshold, kernel, iterations=1)
        # Dilate to get a mask of where letter like structures remain
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (4, 3))
        new_img = cv2.dilate(new_img, kernel, iterations=11)
        # Get all contours
        contours, _ = cv2.findContours(new_img, cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_SIMPLE)
        # Loop through the contours and OCR sub images
        for contour in contours:
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)

            if w < 30 or h < 30:
                continue
            try:
                section = img_smooth[y:y + h, x: x + w]

                section_img = Image.fromarray(section)
                txt = pytesseract.image_to_string(section_img)
                if txt:
                    self.respond(txt)
            except TesseractError:
                pass

