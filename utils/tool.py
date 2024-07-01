import random
import string


## 生辰一个邀请码，8位
def generate_invitation_code(length=8):
    characters = string.ascii_letters + string.digits
    invitation_code = "".join(random.choice(characters) for _ in range(length))
    return invitation_code
