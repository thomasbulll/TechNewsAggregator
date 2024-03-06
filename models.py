class User:
    def __init__(self, id, username, email, is_active=True):
        self.id = id
        self.username = username
        self.email = email
        self.is_active = is_active
        
    def __repr__(self):
        return f'User: {self.username}'
    
    def username(self):
        return self.username
    
    def get_id(self):
        return str(self.id)
    
    def get_email(self):
        return self.email
    
    def is_authenticated(self):
        return self.is_active
