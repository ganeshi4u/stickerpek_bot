import logging
import os
import math
import cv2
import numpy as np
from PIL import Image

from telegram import Sticker
from telegram import Document
from telegram.error import BadRequest
from telegram.error import TelegramError

from bot import u
from .database import Database
from config import config

logger = logging.getLogger(__name__)


def get_correct_size(sizes):
    i = 0 if sizes[0] > sizes[1] else 1  # i: index of the biggest size
    new = [None, None]
    new[i] = 512
    rateo = 512 / sizes[i]
    # print(rateo)
    new[1 if i == 0 else 0] = int(math.floor(sizes[1 if i == 0 else 0] * round(rateo, 4)))

    logger.debug('correct sizes: %dx%d', new[0], new[1])
    return tuple(new)


class StickerFile:

    def __init__(self, sticker, caption=None):
        self._file = sticker
        self._downloaded_file_path = None
        self._png_path = None
        self._emoji = None
        self._size_original = (0, 0)
        self._size_resized = (0, 0)
        self._subdir = ''

        if isinstance(sticker, Sticker):
            logger.debug('StickerFile object is a Sticker')
            self._is_sticker = True
            self._emoji = sticker.emoji if sticker.emoji is not None else '💈'
        elif isinstance(sticker, Document):
            logger.debug('StickerFile object is a Document')
            self._is_sticker = False
            if caption:
                self._emoji = u.get_emojis(caption)
            if not self._emoji:
                self._emoji = '💈'

    @property
    def png_path(self):
        return self._png_path

    @property
    def emoji(self):
        return self._emoji

    @property
    def png_bytes_object(self):
        return self.get_png_bytes_object()

    @property
    def size(self):
        if self._size_resized == (0, 0):
            return self._size_original
        else:
            return self._size_resized

    def download(self, update, prepare_png=False, subdir=''):
        logger.debug('downloading sticker')
        new_file = self._file.get_file()

        if self._is_sticker:
            self._downloaded_file_path = 'tmp/{}downloaded_{}.webp'.format(subdir, self._file.file_id)
        else:  # if we are already working with a png document
            self._downloaded_file_path = 'tmp/{}downloaded_{}.png'.format(subdir, self._file.file_id)

        logger.debug('download path: %s', self._downloaded_file_path)
        new_file.download(self._downloaded_file_path)

        if prepare_png:
            return self.prepare_png(update, subdir=subdir)

    def prepare_png(self, update, subdir=''):
        logger.info('preparing png (source file: %s)', self._downloaded_file_path)

        im = cv2.imread(self._downloaded_file_path)
        transparency_state = Database(config.sqlite.filename).get_transparency_state(update.effective_user.id)

        # transparency parameters
        BLUR = 21
        CANNY_TRESH_1 = 10
        CANNY_TRESH_2 = 200
        MASK_DILATE_ITER = 25
        MASK_ERODE_ITER = 25
        MASK_COLOR = (0.0,0.0,1.0)

        logger.debug('original image size: %s', im.size)
        self._size_original = im.size
        if (np.size(im, 0) > 512 or np.size(im, 1) > 512) or (np.size(im, 0) != 512 and np.size(im, 1) != 512):
            logger.debug('resizing file because one of the sides is > 512px or at least one side is not 512px')
            correct_size = get_correct_size(np.size(im))
            self._size_resized = correct_size
            im = cv2.resize(im, dsize=(correct_size[0], correct_size[1]))
        else:
            logger.debug('original size is ok')

        if 'on' in transparency_state:
            # Read image
            #im = cv2.imdecode(im)
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            # Edge detection
            edges = cv2.Canny(gray, CANNY_TRESH_1, CANNY_TRESH_2)
            edges = cv2.dilate(edges, None)
            edges = cv2.erode(edges, None)

            # contours in edges, sort by area
            contour_info = []
            contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            # Previously, for a previous version of cv2, this line was: 
            #  contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            # Thanks to notes from commenters, I've updated the code but left this note
            for c in contours:
                contour_info.append((
                    c,
                    cv2.isContourConvex(c),
                    cv2.contourArea(c),
                ))
            contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
            max_contour = contour_info[0]

            #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
            # Mask is black, polygon is white
            mask = np.zeros(edges.shape)
            cv2.fillConvexPoly(mask, max_contour[0], (255))

            #-- Smooth mask, then blur it --------------------------------------------------------
            mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
            mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
            mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
            mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

            #-- Blend masked img into MASK_COLOR background --------------------------------------
            mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
            im         = im.astype('float32') / 255.0                 #  for easy blending

            masked = (mask_stack * im) + ((1-mask_stack) * MASK_COLOR) # Blend
            masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit

            # split image into channels
            c_red, c_green, c_blue = cv2.split(im)

            # merge with mask got on one of a previous steps
            im_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0))
            
            self._png_path = 'tmp/{}transparency_converted_{}.png'.format(subdir, self._file.file_id)
        else:
            self._png_path = 'tmp/{}converted_{}.png'.format(subdir, self._file.file_id)

        logger.debug('saving PIL image object as png (%s)', self._png_path)
        cv2.imwrite(self._png_path, im_a*255)

        return self._png_path

    def get_png_bytes_object(self):
        return open(self._png_path, 'rb')

    def delete(self, keep_result_png=False):
        try:
            logger.debug('deleting sticker file: %s', self._downloaded_file_path)
            os.remove(self._downloaded_file_path)
            if not keep_result_png:
                logger.debug('deleting sticker file: %s', self._png_path)
                os.remove(self._png_path)
        except:
            logger.error('error while trying to delete sticker files', exc_info=True)

    def add_to_set(self, bot, user_id, pack_name):
        logger.debug('adding sticker to set %s', pack_name)

        try:
            bot.add_sticker_to_set(
                user_id=user_id,
                name=pack_name,
                emojis=self._emoji,
                png_sticker=self.png_bytes_object,
                mask_position=None
            )
            return 0
        except (BadRequest, TelegramError) as e:
            logger.error('Telegram exception while trying to add a sticker to %s: %s', pack_name, e.message)
            error_code = u.get_exception_code(e)
            if error_code == 0:  # unknown error
                return e.message

            return error_code

    def remove_from_set(self, bot):
        logger.debug('removing sticker from set %s', self._file.set_name)

        try:
            bot.delete_sticker_from_set(self._file.file_id)
            return 0
        except (BadRequest, TelegramError) as e:
            logger.error('Telegram exception while trying to remove a sticker from %s: %s', self._file.set_name,
                         e.message)
            error_code = u.get_exception_code(e)
            if error_code == 0:  # unknown error
                return e.message

            return error_code

    def __repr__(self):
        return 'StickerFile object of original type {} (original size: {}, resized: {})'.format(
            'Sticker' if self._is_sticker else 'Document',
            self._size_original,
            self._size_resized
        )
