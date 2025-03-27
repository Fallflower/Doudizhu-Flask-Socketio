import json
import uuid
import hashlib


class User:

    filename = 'app/user.json'
    list = []

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
        self.list.append(self.__to_dict())

    @classmethod
    def load(cls):
        try:
            with open(cls.filename, 'r') as f:
                cls.list = json.load(f)
        except FileNotFoundError:
            with open(cls.filename, 'w') as f:
                json.dump(cls.list, f)
        # print(cls.list)

    @classmethod
    def save(cls):
        with open(cls.filename, 'w') as f:
            json.dump(cls.list, f, indent=4)

    @classmethod
    def check(cls, name, password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        for user in cls.list:
            if user['name'] == name and user['password'] == hashed_password:
                return user
        return None

    @classmethod
    def register(cls, name, password):
        for user in cls.list:
            if user['name'] == name:
                return False
        user = User(name, password)
        user.__add_user()
        cls.save()
        return True


# if __name__ == '__main__':
#     User.load()
#     User.register('lhy', '123456')
#     print(User.list)
#     User.save()
