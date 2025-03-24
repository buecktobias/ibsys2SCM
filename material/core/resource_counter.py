from collections import Counter

from material.db.models.item import Item

type ItemCounter = Counter[Item]
