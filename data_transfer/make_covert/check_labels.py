# coding: utf-8
# author: hxy
# 2020-6-15
"""
检查标签文件的内容；
删除标件中没有坐标信息的txt文件以及照片文件；
"""
import os
empty_txt = list()


def check_file(labels_folder, images_folder):
    labels = os.listdir(labels_folder)
    for label in labels:
        name = label.split('.')[0]
        size = os.path.getsize(os.path.join(labels_folder, label))
        if size == 0:
        # 确保数据备份，谨慎使用os.remove
            os.remove(os.path.join(labels_folder, name + '.txt'))
            os.remove(os.path.join(images_folder, name + '.jpg'))
            empty_txt.append(name)
    return empty_txt


if __name__ == '__main__':
    empty_list = check_file('E:/yolor-main/yolor-main/bdd100k/train/labels',
                            'E:/yolor-main/yolor-main/bdd100k/train/images')
    print(empty_list)

