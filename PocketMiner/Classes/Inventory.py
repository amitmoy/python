import random


class Item:
    def __init__(self, name, type, baseValue):
        self.name = name
        self.type = type
        self.baseValue = baseValue


class Tool(Item):
    DAMAGEDIFF = 0.3

    def __init__(self, name, baseValue, damage, durability, cost, efficiency):
        Item.__init__(self, name, "tool", baseValue)
        self.damage = damage
        self.maxDurability = durability
        self.durability = durability
        self.cost = cost
        self.efficiency = efficiency

    def generate_damage(self):
        highDamage = int(self.damage * (1 + self.DAMAGEDIFF))
        lowDamage = int(self.damage * (1 - self.DAMAGEDIFF))
        return random.randrange(lowDamage, highDamage)

    def get_value(self):
        return (0.5 * self.baseValue) + (0.5 * self.baseValue * (self.durability / self.maxDurability))

    def use_tool(self):
        if self.durability > 0:
            self.durability -= 5
            return self.generate_damage()

    def get_cost(self):
        return self.cost

    def get_durability(self):
        return self.durability

    def get_max_durability(self):
        return self.maxDurability

    def get_efficiency(self):
        return self.efficiency

    def get_name(self):
        return self.name