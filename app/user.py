import json
import uuid
import hashlib


class User:

    user_file = 'app/user.json'
    users_list = []

    def __init__(self, name, password):
        self.name = name
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.uid = uuid.uuid4()

    def __to_dict(self):
        return {
            'uid': str(self.uid),
            'name': self.name,
            'password': self.password
        }

    def __to_dict__(self):
        return {
            'uid': str(self.uid),
            'name': self.name,
        }

    def __add_user(self):
        self.users_list.append(self.__to_dict())

    @classmethod
    def load(cls):
        try:
            with open(cls.user_file, 'r') as f:
                cls.users_list = json.load(f)
                # for user in cls.users_list:
        except FileNotFoundError:
            with open(cls.user_file, 'w') as f:
                json.dump(cls.users_list, f)

    @classmethod
    def save(cls):
        with open(cls.user_file, 'w') as f:
            json.dump(cls.users_list, f, indent=4)

    @classmethod
    def check(cls, name, password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        for user in cls.users_list:
            if user['name'] == name and user['password'] == hashed_password:
                return user
        return None

    @classmethod
    def register(cls, name, password):
        user = User(name, password)
        user.__add_user()


if __name__ == '__main__':
    User.load()
    User.register('lhy', '123456')
    print(User.users_list)
    User.save()
