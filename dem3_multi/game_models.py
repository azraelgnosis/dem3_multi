from dem3_multi.models import Model
from xml.etree.ElementTree import Element

class Game_Model(Model):
    lists = ()

    def _split_lists(self):
        for prop in self.lists:
            split_list = self._split_list(getattr(self, prop))
            setattr(self, prop, split_list)

    @classmethod
    def from_xml(cls, xml:Element):
        new_model = cls()
        
        return new_model

    @staticmethod
    def _split_list(prop:str) -> list:
        """
        Splits `prop` into a list of ints or floats.
        :prop: a string consisting of a number of comma separated numbers
        :return: a list of ints or floats
        """
        split_list = []

        try:
            split_list = [int(val) for val in prop.split(',')[:-1]]
        except ValueError:
            split_list = [float(val) for val in prop.split(',')[:-1]]

        return split_list


class Party(Game_Model): ...

class Voter(Game_Model):...
    

class Policy(Game_Model):
    __slots__ = [
        'name', 'implementation', 'value', 'history', 'active_history', 'active', 'cost_mult', 'income_mult', 'cost_history', 'income_history', 'earn_scalar', 'cost_scalar',
        'department'    
    ]
    tags = ('name', 'imp', 'targ', 'val', 'history', 'activehistory', 'active', 'cost_mult', 'incom_mult', 'costhistory', 'incomehistory', 'earn_scalar', 'cost_scalar')
    lists = ('history', 'active_history', 'cost_history', 'income_history')

    mapping = {
        'imp': 'implementation',
        'targ': 'target',
        'val': 'value',
        'activehistory': 'active_history',
        'incom_mult': 'income_mult',
        'costhistory': 'cost_history',
        'incomehistory': 'income_history'
    }

    # def _split_lists(self):
    #     self.history = super._split_list(self.history, float) # [float(num) for num in self.history.split(',')]
    #     self.active_history = super._split_list(self.active_history) # [int(num) for num in self.active_history.split(',')]
    #     self.cost_history = super._split_list(self.cost_history, float) # [float(num) for num in self.cost_history.split(',')]
    #     self.income_history = super._split_list(self.income_history, float)

    @staticmethod
    def from_xml(xml:Element) -> 'Policy':
        new_policy = Policy()

        for tag in list(xml):
            tag_name = tag.tag
            setattr(new_policy, Policy.mapping.get(tag_name, tag_name), tag.text)

        new_policy._split_lists()

        return new_policy