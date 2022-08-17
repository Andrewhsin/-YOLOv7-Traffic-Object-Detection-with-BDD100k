import xml.etree.ElementTree as ET
import os
import json

coco = dict()
coco['images'] = []
coco['type'] = 'instances'
coco['annotations'] = []
coco['categories'] = []

category_set = dict()
image_set = set()

category_item_id = 0
image_id = 20200000000
annotation_id = 0


def addCatItem(name):
    global category_item_id
    category_item = dict()
    category_item['supercategory'] = 'none'
    category_item_id += 1
    category_item['id'] = category_item_id
    category_item['name'] = name
    coco['categories'].append(category_item)
    category_set[name] = category_item_id
    return category_item_id


def addImgItem(file_name, size):
    global image_id
    if file_name is None:
        raise Exception('Could not find filename tag in xml file.')
    if size['width'] is None:
        raise Exception('Could not find width tag in xml file.')
    if size['height'] is None:
        raise Exception('Could not find height tag in xml file.')
    image_id += 1
    image_item = dict()
    image_item['id'] = image_id
    image_item['file_name'] = file_name
    image_item['width'] = size['width']
    image_item['height'] = size['height']
    coco['images'].append(image_item)
    image_set.add(file_name)
    return image_id


def addAnnoItem(object_name, image_id, category_id, bbox):
    global annotation_id
    annotation_item = dict()
    annotation_item['segmentation'] = []
    seg = []
    # bbox[] is x,y,w,h
    # left_top
    seg.append(bbox[0])
    seg.append(bbox[1])
    # left_bottom
    seg.append(bbox[0])
    seg.append(bbox[1] + bbox[3])
    # right_bottom
    seg.append(bbox[0] + bbox[2])
    seg.append(bbox[1] + bbox[3])
    # right_top
    seg.append(bbox[0] + bbox[2])
    seg.append(bbox[1])

    annotation_item['segmentation'].append(seg)

    annotation_item['area'] = bbox[2] * bbox[3]
    annotation_item['iscrowd'] = 0
    annotation_item['ignore'] = 0
    annotation_item['image_id'] = image_id
    annotation_item['bbox'] = bbox
    annotation_item['category_id'] = category_id
    annotation_id += 1
    annotation_item['id'] = annotation_id
    coco['annotations'].append(annotation_item)


def parseXmlFiles(xml_dir, path_save_txt):
    cnt_8 = 0
    for f in os.listdir(xml_dir):
        if not f.endswith('.xml'):
            continue

        file_name = None

        xml_file = os.path.join(xml_dir, f)
        # xml_file = "/data_1/everyday/0120/biaozhu/item_000000210.xml"
        cnt_8 += 1;
        print(cnt_8, "   ", xml_file)

        L_all = []
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != 'annotation':
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))

        # elem is <folder>, <filename>, <size>, <object>
        for elem in root:
            current_parent = elem.tag

            if "object" == elem.tag:
                aa = 0

            # if elem.tag == 'folder':
            #    continue

            if elem.tag == 'filename':
                file_name = elem.text

            L = []
            if elem.tag == 'object':
                for sub_elem in elem:
                    sub_elem_tag = sub_elem.tag
                    if "polygon" == sub_elem_tag:
                        for elem_polygon in sub_elem:
                            elem_pt = elem_polygon.tag
                            if "pt" == elem_pt:
                                dict_1 = {}
                                for elem_pt_sub in elem_polygon:
                                    dict_1[elem_pt_sub.tag] = int(float(elem_pt_sub.text))
                                L.append((dict_1["x"], dict_1["y"]))
            if len(L) > 0:
                L_all.append(L)

        path_save_txt_ = path_save_txt + file_name.replace(".jpg", ".txt")
        with open(path_save_txt_, "w") as fw:
            for line in L_all:
                for cnt, pt in enumerate(line):
                    fw.write(str(pt[0]))
                    fw.write(",")
                    fw.write(str(pt[1]))
                    if cnt == len(line) - 1:
                        fw.write("\n")
                    else:
                        fw.write(",")

        bbb = 0


if __name__ == '__main__':
    xml_dir = 'E:/yolor-main/cancer/xml'
    path_save_txt = "E:/yolor-main/cancer/train.txt"
    parseXmlFiles(xml_dir, path_save_txt)
    # json.dump(coco, open(json_file, 'w'))
