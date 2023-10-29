class Person():
    def __init__(self, row):
        self._id = row[0]
        self._name = row[1]
        self._surname = row[2]
        self._dni = row[3]
        self._email = row[4]

    def to_json(self):
        return {
            "id": self._id,
            "name": self._name,
            "surname": self._surname,
            "dni": self._dni,
            "email": self._email
        }
