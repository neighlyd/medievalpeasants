from faker.providers import BaseProvider
import random

'''
    factory_boy does not have a faker provider to autogenerate choices using Django's choice fields. 
    You need to create a faker provider for it using a class method.
    This may be resolved in a future version, though this issue has been outstanding since August, 2016:
    https://github.com/FactoryBoy/factory_boy/issues/271 
'''

class ChoiceProvider(BaseProvider):
    def random_choice(self, choices):
        '''
        Given a list of choices in Django format, return a random value.
        '''
        choice = self.random_element(choices)
        return choice[0]

class RelationProvider(BaseProvider):
    def relation_choice(self):
        relation = ['son of', 'daughter of', '']
        return random.choice(relation)

class FolioProvider(BaseProvider):
    def folio(self):
        if random.random() < .5:
            return str(random.randint(1, 75))+'v'
        else:
            return str(random.randint(1, 75))