import random
import string

def generate_invitee_code():
    code_length = 8
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choices(characters, k=code_length))
    return code
