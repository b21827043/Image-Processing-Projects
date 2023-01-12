import os

image_list = os.listdir(os.path.join(os.getcwd(),"images"))
label_list = os.listdir(os.path.join(os.getcwd(),"labels"))

deleted_images = list()

#Deleted Unlabeled Images
for i in image_list:
    temp = i.split(".")
    if temp[0]+".txt" in label_list:
        pass
    else :
        deleted_images.append(i)

for i in deleted_images:
    os.remove(os.path.join(os.getcwd(),"images",i))
