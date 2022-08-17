import utils.autoanchor as autoAC

new_anchors = autoAC.kmean_anchors('E:/yolov7-main/data/bdd100k.yaml', 12, 1280, 4.0, 30000, True)
print(new_anchors)