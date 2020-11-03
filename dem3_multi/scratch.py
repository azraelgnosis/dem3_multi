import os
import xml.etree.ElementTree as ET
import re

def load_save_file(filename:str):
    """
    """

    save_path = r"C:\Users\root\Documents\My Games\democracy3\savegames"
    # filename = "test1.xml"

    with open(os.path.join(save_path, filename), "r") as f:
        xml = f.read()

    xml = "<xml>\n" + xml # add opening <xml> tag to complement end tag

    # replaces <0>...</0> with <_0>...</_0> and <0_hist>...</0_hist> with <_0_hist>...</_0_hist>
    xml = re.sub(r"<(\d{1,2}(?:_hist)?>)(.*)</(\d{1,2}(?:_hist)?>)", r"<_\1\2</_\3", xml)

    root = ET.fromstring(xml)
    load_data = root.find("load_data")
    date = root.find('.//date').text
    country = root.find('.//name').text

    votersA = root.find('voters').findall('voter')
    votersB = list(root.find('voters'))
    votersC = [voter for voter in root.find('voters').iter('voter')]
    votersD = [voter for voter in root.find('voters').iterfind('voter')]

    print("done")

load_save_file("test1.xml")