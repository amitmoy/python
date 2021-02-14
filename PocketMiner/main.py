from Classes.game import Person, BColors, Stone
from Classes.Inventory import Tool, Item

'''tools = [{"name": "Stone Pickaxe", "cost": 5, "damage": 20,
          "efficiency": 0.1, "durability": 100, "maxDurability": 100},
         {"name": "Bronze Pickaxe", "cost": 10, "damage": 50,
          "efficiency": 0.3, "durability": 50, "maxDurability": 50},
         {"name": "Diamond Pickaxe", "cost": 20, "damage": 120,
          "efficiency": 0.7, "durability": 20, "maxDurability": 20}]'''

tools = [Tool("Stone Pickaxe", 50, 20, 100, 5, 1),
         Tool("Iron Pickaxe", 100, 50, 80, 10, 3),
         Tool("Diamond Pickaxe", 300, 100, 50, 20, 10)]

player = Person(0, [], 1000, tools)
rock = Stone(1000)
'''
player.show_actions()
print("damage:", player.use_tool(1))
player.show_actions()
print("damage:", player.use_tool(1))
player.show_actions()
print("damage:", player.use_tool(1))
player.show_actions()
'''

while True:
    player.show_actions()
    playerInput = input(BColors.OKBLUE + BColors.UNDERLINE + "Choose Tool:" + BColors.ENDC)
    print("damage:", player.use_tool(int(playerInput), rock), "to rock:", rock.get_hp())
