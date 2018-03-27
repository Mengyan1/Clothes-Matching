import cv2
import matplotlib.pyplot as plt
import constant
import util
from clothes_matcher import ItemKNNMatcher
import sys


def show_picture(item_list):
    item_infos = util.load_item_info(constant.ITEM_FILE, constant.ITEM_IMAGE_PATHS)
    plt.subplot()
    for index, item in enumerate(item_list):
        img_path = item_infos[item]._item_image_path
        img = cv2.imread(img_path ,1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img)
        plt.title(item)
        plt.xticks([])
        plt.yticks([])
        plt.show()

if __name__ == '__main__':
    matcher = ItemKNNMatcher()
    result = matcher.find_matched_clothes(sys.argv[1], 10)
    print ('Final Recommendation:', result)
    show_picture([sys.argv[1]])
    show_picture(result)
        






