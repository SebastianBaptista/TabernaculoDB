
class Member():
    def __init__(self,DNI,full_name,age,phone,occupation,occupation_place,knowledge,vehicle,responsabilities,civil_status,childrens,nationality,hierarchy,situation,id_member):
        super().__init__()
        self.full_name=full_name
        self.age=age
        self.occupation=occupation
        self.occupation_place=occupation_place
        self.childrens=childrens
        self.DNI=DNI
        self.civil_status=civil_status
        self.knowledge=knowledge
        self.responsabilities=responsabilities
        self.vehicle=vehicle
        self.phone=phone
        self.hierarchy=hierarchy
        self.nationality=nationality
        self.situation=situation
        self.id_member=id_member