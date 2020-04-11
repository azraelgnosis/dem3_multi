from flask import g
import os
import re
import xml.etree.ElementTree as ET

from dem3_multi.game_models import Policy

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

def get_policies() -> list:
    game = load_save_file()

    policies = game.find(".//policies")
    policies = [Policy.from_xml(policy) for policy in policies.iter('policy')]

    return policies

def get_policy(policy_name:str) -> Policy:
    """
    Finds and returns the specified Policy object.

    `policy_name`: Name of the policy being retrieved.

    Return the Policy object matching `policy_name`.
    """
    policies = get_policies()
    policy = next(filter(lambda p: p.name == policy_name, policies))

    return policy



