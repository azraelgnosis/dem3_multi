from dem3_multi.models import Model
from xml.etree.ElementTree import Element

class Game_Model(Model):
    lists = ()
    #? Might be a problem when it's time to write to file
    mapping = {
        'imp': 'implementation',
        'targ': 'target',
        'val': 'value',
        'activehistory': 'active_history',
        'incom_mult': 'income_mult',
        'costhistory': 'cost_history',
        'incomehistory': 'income_history',
        'fullname': 'name'
    }

    def __init__(self):
        self.name = None

    def _split_lists(self):
        for prop in self.lists:
            split_list = self._split_list(getattr(self, prop))
            setattr(self, prop, split_list)

    @classmethod
    def from_xml(cls, xml:Element):
        new_model = cls()

        for tag in list(xml):
            tag_name = tag.tag
            tag_text = Game_Model._coerce_type(tag.text)
            setattr(new_model, Game_Model.mapping.get(tag_name, tag_name), tag_text)
        
        new_model._split_lists()
        
        return new_model

    @staticmethod
    def _split_list(prop:str) -> list:
        """
        Splits `prop` into a list of ints or floats.
        :prop: a string consisting of a number of comma separated numbers
        :return: a list of ints or floats
        """
        split_list = []

        #? maybe the values should remain as strings
        split_list = [Game_Model._coerce_type(val) for val in prop.split(',')[:-1]]
        split_list.reverse()
        # try:
        #     split_list = [int(val) for val in prop.split(',')[:-1]]
        # except ValueError:
        #     split_list = [float(val) for val in prop.split(',')[:-1]]

        return split_list

    @staticmethod
    def _coerce_type(val):
        try:
            val = int(val)
        except ValueError:
            try:
                val = float(val)
            except ValueError: 
                pass
        return val

    def __repr__(self): return f"{self.name}"


class Party(Game_Model): ...
class Voter(Game_Model): ...

class VoterType(Game_Model):
    lists = ('history', 'perc_history')
    active = True

class Policy(Game_Model):
    __slots__ = [
        'name', 'descripion', 'implementation', 'value', 'history', 'active_history', 'active', 'cost_mult', 'income_mult', 'cost_history', 'income_history', 'earn_scalar', 'cost_scalar',
        'department'    
    ]
    tags = ('name', 'imp', 'targ', 'val', 'history', 'activehistory', 'active', 'cost_mult', 'incom_mult', 'costhistory', 'incomehistory', 'earn_scalar', 'cost_scalar')
    lists = ('history', 'active_history', 'cost_history', 'income_history')

    

    def __init__(self):
        self.name = None

    # @staticmethod
    # def from_xml(xml:Element) -> 'Policy':
    #     new_policy = Policy()

    #     for tag in list(xml):
    #         tag_name = tag.tag
    #         tag_text = tag.text
            

    #         setattr(new_policy, super.mapping.get(tag_name, tag_name), tag_text)

    #     new_policy._split_lists()

    #     return new_policy

    def __repr__(self): return f"{self.name}"

class Situation(Game_Model):
    lists = ('history', 'active_history')
#     @staticmethod
#     def from_xml(xml:Element) -> 'Situation':
#         new_situation = Situation()

#         for tag in list(xml):
#             tag_name = tag.tag
#             tag_text = super._coerce_type(tag.text)

#             setattr(new_situation, super.mapping.get(tag_name, tag_name), tag_text)

#             new_situation._split_lists()

#             return new_situation


class Dilemma(Game_Model): ...

class Simvalue(Game_Model):
    lists = ['history']
    active = True

class Grudge(Game_Model): ...
class Minister(Game_Model): ...
class PressureGroup(Game_Model): ...

class Save(Game_Model):
    __slots__ = ["filename", "policies"]