from flask import g
import os
import re
import xml.etree.ElementTree as ET

from dem3_multi.game_models import Minister, Policy, Simvalue, Situation, VoterType

mapping = {
    'ministers': {
        'subtype': 'minister',
        'class': Minister
    },
    'policies': {
        'subtype': 'policy',
        'class': Policy
    },
    'simvalues': {
        'subtype': 'simvalue',
        'class': Simvalue
    },
    'situations': {
        'subtype': 'situation',
        'class': Situation
    },
    'votertypes': {
        'subtype': 'votertype',
        'class': VoterType
    }
}

#TODO
def load_save_file(filename:str="test3.xml") -> ET.Element:
    """
    """

    if 'save' not in g:
        save_path = r"C:\Users\root\Documents\My Games\democracy3\savegames"

        with open(os.path.join(save_path, filename), "r") as f:
            xml = f.read()

        xml = "<xml>\n" + xml # add opening <xml> tag to complement end tag

        # replaces <0>...</0> with <_0>...</_0> and <0_hist>...</0_hist> with <_0_hist>...</_0_hist>
        xml = re.sub(r"<(\d{1,2}(?:_hist)?>)(.*)</(\d{1,2}(?:_hist)?>)", r"<_\1\2</_\3", xml)

        root = ET.fromstring(xml)

        g.save = root
    
    return g.save

def get_game_data(datatype:str) -> list:
    """
    """

    save = load_save_file()
    data = save.find(f".//{datatype}")
    
    Class = mapping.get(datatype)['class']
    subtype = mapping.get(datatype)['subtype']
    data = [Class.from_xml(datum) for datum in data.iter(subtype)]

    return data

def get_game_datum(datatype:str, data_name:str):
    """
    """
    
    data = get_game_data(datatype)
    datum = next(filter(lambda d: d.name == data_name, data))

    return datum

def get_finances():
    """
    """

    save = load_save_file()
    finances = save.find(f".//finances")

    return