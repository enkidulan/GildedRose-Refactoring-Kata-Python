from dataclasses import dataclass
from enum import StrEnum


class ItemType(StrEnum):
    REGULAR = "REGULAR"
    AGED = "AGED"
    LEGENDARY = "LEGENDARY"
    BACKSTAGE_PASS = "BACKSTAGE_PASS"
    CONJURED = "CONJURED"


@dataclass
class Item:
    name: str
    sell_in: int
    quality: int
    item_type: ItemType = ItemType.REGULAR

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


@dataclass
class ItemRule:

    def get_degree(self, item: Item):
        return -2 if item.sell_in < 0 else -1

    def calculate_new_quality(self, item: Item):
        degree = self.get_degree(item)
        quality = item.quality + degree
        if quality < 0:
            quality = 0
        elif quality > 50:
            quality = 50
        return quality

    def update(self, item: Item):
        item.sell_in -= 1
        item.quality = self.calculate_new_quality(item)


class ConjuredItemRule(ItemRule):
    def get_degree(self, item: Item):
        return super().get_degree(item) * 2


class IncreasingQualityItemRule(ItemRule):
    def get_degree(self, item: Item):
        return -super().get_degree(item)


class LegendaryItemRule(ItemRule):
    def update(self, _):
        pass


class BackstagePassItemRule(IncreasingQualityItemRule):
    def get_degree(self, item: Item):
        if item.sell_in < 0:
            return -item.quality
        elif item.sell_in < 5:
            return 3
        elif item.sell_in < 10:
            return 2
        return 1


names_mapping = {}

type_mapping = {
    ItemType.REGULAR: ItemRule,
    ItemType.AGED: IncreasingQualityItemRule,
    ItemType.LEGENDARY: LegendaryItemRule,
    ItemType.BACKSTAGE_PASS: BackstagePassItemRule,
    ItemType.CONJURED: ConjuredItemRule,
}


def get_rule(item: Item):
    return type_mapping.get(item.name, type_mapping[item.item_type])


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            rule = get_rule(item)()
            rule.update(item)
