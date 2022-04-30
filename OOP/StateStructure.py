"""
State(from City): 
    1, financial 2, defence 3, domestics 4, diplomacy 5, productivity 6, people 
    7, reputation 8, city 9, public_will
City:
    1, attribution 2, condition 3, public_will 4, area 5, terrain 6, public_security
Policy(domestic&diplomatic): 
    1, radical 2, steady 3, appeasement 4, isolate 5, aggression 6, alliance 7, vassal
    8, rehabilitate

People: I, age II, career:
        1, worker 2, soldier 3, police 4, doctor 5, scientist 6, farmer 
        7, gangster/mafia 8, (spy) 9, merchant
        III, born rate IV, death rate
Hero(from people's career):
        I carrer:
        1, Craftsman 2, General 3, Detective 4, Recover 5, Genius 6, Agriculture 
        7, Godfather 8, Defection 9, Trader
        II 
Army(soldier):
    1, engineer 2, warrior 3, medical 4, logistic 5, signal 6, scout 7, artillery 8, assault
War:
    1, troops 2, rations 3, construction 4, strategy 5, firepower(buildings) 6, cure 
    7, casualty(army)
"""
class City(object):
    def __init__(self, city_level: int, state_name: str, terrain: str) -> None:
        self.financial = city_level * 1000
        self.defence = city_level * 100
        self.public_security = city_level
        self.productivity = city_level * 1000
        self.people = city_level * 100
        self.reputation = city_level
        self.attribution = state_name
        self.condition = 100
        self.public_will = 100
        self.area = city_level
        self.terrain = terrain
        self.public_security = 100

    @property   
    def financial(self) -> int:
        self.financial = worker + merchant * 10 - self.expenditure
        return self.financial
    @property
    def productivity(self) -> int:
        self.productivity = self.area * 1000 - self.people
        return self.productivity
    @property
    def defence(self) -> int:
        return self.defence - war_injure
    @property
    def expenditure(self) -> int:
        return 

class State(City):
    def __init__(self, city_level: int) -> None:
        super().__init__(city_level)
        self.diplomacy = 0 # how many states are built relationship with
        self.city = 1
        self.domestics = city_level * 100

class People(object):
    def __init__(self) -> None:
        self.