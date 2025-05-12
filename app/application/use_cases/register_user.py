from app.domain.entities.user import User
from app.domain.enums import UserRole
from datetime import datetime
import uuid


class RegisterUserUseCase:
    def __init__(self, user_repository, auth_service):
        self.user_repository = user_repository
        self.auth_service = auth_service
        
    def execute(self, name, email, password): 
        # Check if email already exists
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Hash the password
        hashed_password = self.auth_service.hash_password(password)
        
        # Create new user with patient role
        new_user = User(
            id=str(uuid.uuid4()),
            name=name,
            email=email.lower(),  # Store email in lowercase for consistency
            hashed_password=hashed_password,
            role=UserRole.PATIENT,  # Always set as patient
            specialization=None,  # Patients don't have specialization
            created_at=datetime.now()
        )

        self.user_repository.save(new_user)
        return new_user