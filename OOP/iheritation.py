class Family(object):
    def __init__(self, family_name: str) -> None:
        self._family_name = family_name
    
    @property
    def give_generation_name(self) -> str:
        return self._generation_name

    @give_generation_name.setter
    def give_generation_name(self, name: str) -> None:
        self._generation_name = name

class Parents(Family):
    def __init__(self, family_name: str) -> None:
        super().__init__(family_name)

    @property
    def give_given_name(self) -> str:
        return self._given_name

    @give_given_name.setter
    def give_given_name(self, name: str) -> None:
        self._given_name = name
        
    @property
    def generation_name(self, name: str) -> None:
        self._2nd_name = name
        return self._2nd_name

    @property
    def given_name(self) -> None:
        return self._3rd_name

    @given_name.setter
    def given_name(self, name: str) -> None:
        self._3rd_name = name


class Sons(Parents):
    def __init__(self, family_name: str) -> None:
        super().__init__(family_name)

class Daughts(Parents):
    def __init__(self, family_name: str) -> None:
        super().__init__(family_name)

if __name__=='__main__':
    Li = Family('Li')
    father = Parents(Li)
    son = Sons(father)
    print(son._family_name)

"""奇琦
    @property
    def job(self, job_name: str) -> None:
        self._job = job_name

    def annual_salary(self, salary: float) -> None:
        self._salary = salary

    def years_of_service(self, year: float) -> None:
        self._year = year

    def assets(self) -> float:
        self.money = self.salary * self._year
        return self.money
"""