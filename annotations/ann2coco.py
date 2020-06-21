# 将txt 标注转换为coco数据集格式
import os
import cv2
import json

lines = []
with open("ann.txt", "r") as f:
	lines = [row.strip() for row in f.readlines()]

file_name = None
category = None
width = 0
height = 0

image_id = 0
ann_id = 0

images = []
annotations = []
categories = ["wheat"]

for index in range(len(lines)):
	line = lines[index]

	if index % 2 == 0:

		file_name, category = line.split(",")
		if not category in categories:
			categories.append(category)
		file_name = file_name + ".jpg"
		img_path = os.path.join("train", file_name)
		
		img = cv2.imread(img_path)
		
		height = img.shape[0]
		width = img.shape[1]
		images.append({"file_name": file_name, "height": height, "width": width, "id": image_id})
		

	else:
		items = line.split(":")
		for item in items:
			bbox = [int(x) for x in item.split(",")]
			ann = {"image_id": image_id, "category_id": categories.index(category), "id": ann_id, "bbox": bbox}
			annotations.append(ann)
			ann_id = ann_id + 1
		image_id = image_id + 1

categories = [{"supercategory": categories[0], "id": index, "name": categories[index]} for index in range(len(categories))]

data_coco = {}
data_coco["annotations"] = annotations
data_coco["images"] = images
data_coco["categories"] = categories

annFile = "wheat_annotations.json"

json.dump(data_coco, open(annFile, "w"), indent=4)



