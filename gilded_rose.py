from dataclasses import dataclass


@dataclass
class Item:
    name: str
    sell_in: int
    quality: int

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


@dataclass
class ItemRule:

    item: Item

    def change_quality(self, degree):
        if not (0 <= self.item.quality <= 50):
            return
        self.item.quality += degree
        if self.item.quality < 0:
            self.item.quality = 0
        if self.item.quality > 50:
            self.item.quality = 50

    def get_degree(self):
        return -2 if self.item.sell_in < 0 else -1

    def update(self):
        self.item.sell_in -= 1
        degree = self.get_degree()
        self.change_quality(degree)


class ConjuredItemRule(ItemRule):
    def get_degree(self):
        return super().get_degree() * 2


class IncreasingQualityItemRule(ItemRule):
    def get_degree(self):
        return -super().get_degree()


class LegendaryItemRule(ItemRule):
    def update(self):
        pass


class BackstagePassItemRule(IncreasingQualityItemRule):
    def get_degree(self):
        if self.item.sell_in < 0:
            return -self.item.quality
        elif self.item.sell_in < 5:
            return 3
        elif self.item.sell_in < 10:
            return 2
        return 1


rules_mapping = {
    "Aged Brie": IncreasingQualityItemRule,
    "Sulfuras, Hand of Ragnaros": LegendaryItemRule,
    "Backstage passes to a TAFKAL80ETC concert": BackstagePassItemRule,
    "Conjured Mana Cake": ConjuredItemRule,
}


def get_rule(item):
    return rules_mapping.get(item.name, ItemRule)(item)


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            rule = get_rule(item)
            rule.update()
