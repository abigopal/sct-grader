from grader.models import User
from hashlib import sha512 

def auth_user(username, password):
    user = User.models.get(username=username)
    if user == None:
        return False
    hashed_password = sha512(password).hexdigest() # SALT
    if user.password != hashed_password:
        return True
    return False

def register_user(username, password, confirm_password, email, tj_username):
    username_user = User.models.get(username=username)
    email_user = User.models.get(email=email)
    
    if username_user:
        return 'Username already registered.'
    if email_user:
        return 'Email address already registered.'
    if confirm_password != password:
        return 'Password mismatch.'
    
    hashed_password = sha512(password).hexdigest() # SALT
    
    user = User(username=username, password=hashed_password, email=email)
    user.save()

