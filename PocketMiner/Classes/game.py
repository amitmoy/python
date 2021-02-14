import random


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, money, items, tools, energy):
        self.money = money
        self.items = items
        self.maxenergy = energy
        self.energy = energy
        self.tools = tools

    def generate_tool_damage(self, i):
        dmgl = int(self.tools[i]["damage"]*0.6)
        dmgh = int(self.tools[i]["damage"]*1.4)
        return random.randrange(dmgl, dmgh)

    def spend_energy(self, num):
        self.energy -= num
        if self.energy < 0:
            self.energy = 0

    def use_tool(self, i):
        self.tools[i]["durability"] -= 5
        self.spend_energy(self.tools[i]["cost"])
        dmg = self.generate_tool_damage(i)
        if self.tools[i]["durability"] <= 0:
            self.tools.pop(i)
        return dmg

    def get_money(self):
        return self.money

    def get_items(self):
        return self.items

    def get_energy(self):
        return self.energy

    def get_tools(self):
        return self.tools

    def get_tool_name(self, i):
        return self.tools[i]["name"]

    def get_tool_cost(self, i):
        return self.tools[i]["cost"]

    def show_actions(self):
        i = 1
        print(BColors.BOLD + BColors.OKGREEN + "Tools" + BColors.ENDC)
        for tool in self.tools:
            print(BColors.OKGREEN + str(i) + ": " + str(tool["name"]) +
                  ", Durability: " + str(tool["durability"]) + "/" + str(tool["maxDurability"]) + BColors.ENDC)
            i += 1


class Stone:
    def __init__(self, hp):
        self.hp = hp
        self.efficiency = 0

    def get_hp(self):
        return self.hp

    def take_damage(self, damage, efficiency):
        self.hp -= damage
        self.efficiency += efficiency
        if self.hp < 0:
            self.hp = 0
            return self.generate_loot()
        return {"name": "stone", "amount": damage}

    def generate_loot(self):
        choice = random.choices(["bronze ore", "iron ore", "gold ore", "diamond ore"], weights=(45, 25, 20, 10), k=1)
        return {"name": choice[0], "amount": self.efficiency}
