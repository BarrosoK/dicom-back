from json import JSONEncoder
import numpy
import os

class numpy_array_encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def is_img_too_small(img):
    if img.shape[0] < int(os.getenv("IMG_DIM_MIN")) or img.shape[1] < int(os.getenv("IMG_DIM_MIN")):
        return True
    return False


def is_img_too_big(img):
    if img.shape[0] > int(os.getenv("IMG_DIM_MAX")) or img.shape[1] > int(os.getenv("IMG_DIM_MAX")):
        return True
    return False
