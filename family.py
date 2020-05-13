import random 

class Family:
    def __init__(self, last_name):
        self._last_name = last_name
        self._members = []

    def _generateId(self):
        return random.randint(0, 99999999)

    def add_member(self, member):
        member['id'] = self._generateId()
        self._members.append(member)

    def delete_member(self, id):
        member = list(filter(lambda person: person['id'] == id, self._members))

        return self._members.remove(member[0])

    def update_member(self, id, member):
        pass

    def get_member(self, id):
        member = list(filter(lambda person: person['id'] == id, self._members))
        if member == []:
            return None
        return member[0]

    def get_all_members(self):
        return self._members