from collections import Counter
from dataclasses import dataclass



@dataclass
class ResourceCounter:
    items: Counter


    def get_number_from_uid(self, uid: str):
        if "." in uid:
            return int(uid.split(".")[0])
        else:
            return int(uid[1:])

    def print_sorted_resources(self):
        for key in sorted(self.items, key=lambda x: self.get_number_from_uid(x)):
            print(f"{key}: {self.items[key]}")

    def get_sorted_items(self):
        return [
            (key, self.items[key])
            for key in sorted(self.items, key=lambda x: self.get_number_from_uid(x))
            if ProductionNodeType.
        ]