from Classes.game import Person, BColors

tools = [{"name": "Stone Pickaxe", "cost": 5, "damage": 20,
          "efficiency": 0.1, "durability": 100, "maxDurability": 100},
         {"name": "Bronze Pickaxe", "cost": 10, "damage": 50,
          "efficiency": 0.3, "durability": 50, "maxDurability": 50},
         {"name": "Diamond Pickaxe", "cost": 20, "damage": 120,
          "efficiency": 0.7, "durability": 20, "maxDurability": 20}]

player = Person(0, [], tools, 100)

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
    print("damage:", player.use_tool(int(playerInput)))
