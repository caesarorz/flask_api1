# users = [
#     {
#         'id'; 1,
#         'username': 'bob',
#         'password': 'abcd'
#     }
# ]

# userid_mapping = { 1: {
#         'id': 1,
#         'username': 'bob',
#         'password': 'abcd'
#     }
# }

# username_mapping = { 'bob': {
#         'id': 1,
#         'username': 'bob',
#         'password': 'abcd'
#     }
# }



# users = [
#     User(1, 'bob', 'abc')
# ]

# username_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}

from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    user = UserModel.find_by_username(username) # user = username_mapping.get(username, None)
    # if user and user.password == password avoid this
    if user and safe_str_cmp(user.password, password): # safe way of compareing strings
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id) # return userid_mapping.get(user_id, None)
