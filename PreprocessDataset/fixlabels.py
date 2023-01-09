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


# Label Class ID Changer
for i in label_list:
    new_string = None
    with open(os.path.join(os.getcwd(),"labels",i),"r+") as r:
        string = r.read()
        print(string)
        string = string.split(" ")
        print(string)
        string[0] = "3"
        print(string)
        new_string = " ".join(string)
        print(new_string)

    with open(os.path.join(os.getcwd(), "labels", i), "w") as w:
        w.write(new_string)





