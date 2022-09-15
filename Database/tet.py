import os
from os import listdir

dirname = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(dirname, os.pardir))
com_path = os.path.join( f"static/images/company_img/AfriGaz_9.jpg")
test = "e:\\New folder (3)\\traveler\\classimax-premium\\static/images/company_img/AfriGaz_9.jpg"
c= test.split("/")
# dir = listdir(com_path)
print(com_path)
print(c)
