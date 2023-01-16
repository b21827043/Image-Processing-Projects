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


deleted_names = []

# Label Class ID Changer
for i in label_list:
    write_text = ""
    with open(os.path.join(os.getcwd(),"labels",i),"r+") as r:

        text = r.read()
        text_split = text.split("\n")

        if text_split[-1] == "":
            text_split.pop()

        for k in text_split:
            split_i = k.split(" ")
            if split_i[0] == "0":
                temp = " ".join(split_i) + "\n"
                write_text += temp
            if split_i[0] in ["1", "2", "3", "5", "7"]:
                split_i[0] = "1"
                temp = " ".join(split_i) + "\n"
                write_text += temp

    with open(os.path.join(os.getcwd(), "labels", i), "w") as w:
        w.write(write_text[:-1])

    if (write_text == ""):
        temp_split = i.split(".")
        deleted_names.append(temp_split[0])


for j in deleted_names:
    os.remove(os.path.join(os.getcwd(),"images",j+".jpg"))
    os.remove(os.path.join(os.getcwd(),"labels",j+".txt"))
