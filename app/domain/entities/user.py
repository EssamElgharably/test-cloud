class User:
    def __init__(self, id, name, email, hashed_password, role, created_at, specialization=None):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.created_at = created_at
        self.specialization = specialization