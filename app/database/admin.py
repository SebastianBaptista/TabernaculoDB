
from werkzeug.security import generate_password_hash, check_password_hash

class Admin():
    def __init__(self,id,email,password,name):
        self.id=id
        self.email=email
        self.password=password
        self.name=name
        
    @classmethod
    def check_password(self, hashed_password,password):
        return check_password_hash(hashed_password,password)
        
    @classmethod
    def generate_hash(self,password):
        return generate_password_hash(password)

