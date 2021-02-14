import random
from .Inventory import Tool, Item


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
    def __init__(self, money, items, energy, tools):
        self.money = money
        self.items = items
        self.maxEnergy = energy
        self.energy = energy
        self.tools = tools

    def spend_energy(self, num):
        self.energy -= num
        if self.energy < 0:
            self.energy = 0

    def use_tool(self, i, rock):
        tool = self.tools[i]
        if tool.get_cost() > self.energy:
            return
        self.spend_energy(tool.get_cost())
        dmg = tool.use_tool()
        efficiency = tool.get_efficiency()
        rock.take_damage(dmg, efficiency)
        if tool.get_durability() <= 0:
            self.tools.pop(i)
        return dmg

    def show_actions(self):
        i = 1
        print(BColors.BOLD + BColors.OKGREEN + "Tools" + BColors.ENDC)
        for tool in self.tools:
            print(BColors.OKGREEN + str(i) + ": " + str(tool.get_name()) +
                  ", Durability: " + str(tool.get_durability()) + "/" + str(tool.get_max_durability()) + BColors.ENDC)
            i += 1

    def get_money(self):
        return self.money

    def get_items(self):
        return self.items

    def get_energy(self):
        return self.energy

    def get_tools(self):
        return self.tools

    def get_tool_name(self, i):
        return self.tools[i].get_name()

    def get_tool_cost(self, i):
        return self.tools[i].get_cost()


class Stone:
    def __init__(self, hp):
        self.hp = hp
        self.efficiency = 0

    def get_hp(self):
        return self.hp

    def take_damage(self, damage, efficiency):
        if self.hp == 0:
            return
        self.hp -= damage
        self.efficiency += efficiency
        if self.hp < 0:
            self.hp = 0
            return self.generate_loot()
        return {"name": "stone", "amount": damage}

    def generate_loot(self):
        choice = random.choices(["bronze ore", "iron ore", "gold ore", "diamond ore"], weights=(45, 25, 20, 10), k=1)
        return {"name": choice[0], "amount": self.efficiency}
