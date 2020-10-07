import cv2
import matplotlib.pyplot as plt


class ImageUtility:
    @staticmethod
    def resize_with_aspect_ratio(image, width=None, height=None,
                                 inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation=inter)

    @staticmethod
    def show(image):
        img_small = ImageUtility.resize_with_aspect_ratio(image, height=600)
        cv2.imshow('img', img_small)

    @staticmethod
    def load_image(path, filename, show=False):
        extension = filename.split('.')[1].lower()
        if extension == 'jpg':
            img = plt.imread(path)
            if show:
                img_cv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                ImageUtility.show(img_cv)
            print(img.shape)
        else:
            img_cv = cv2.imread(path)
            if show:
                ImageUtility.show(img_cv)
            img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            print(img.shape)
        return img
