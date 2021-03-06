from room import Room
from item import Item
from character import Enemy
from character import Character
from character import Friend
from rpginfo import RPGInfo

spooky_castle = RPGInfo("The Spooky Castle")
spooky_castle.welcome()
RPGInfo.info()

backpack = []

kitchen = Room("Kitchen")
ballroom = Room("Ballroom")
dining_hall = Room("Dining Hall")

print("There are " + str(Room.number_of_rooms) + " Rooms to explore.")

# set descriptions of the rooms
kitchen.set_description("A dank and dirty room buzzing with flies.")
ballroom.set_description("A vast room with a shiny wooden floor; huge candlesticks guard the entrance.")
dining_hall.set_description("A large room with ornate golden decorations on each wall.")

# link the rooms
kitchen.link_room(dining_hall, "south")
ballroom.link_room(dining_hall, "east")
dining_hall.link_room(kitchen, "north")
dining_hall.link_room(ballroom, "west")

# set characters
dave = Enemy("Dave", "A smelly zombie!")
dave.set_conversation("Ahhh...I will eat you!")
dave.set_weakness("cheese")

susi = Character("Susi", "A cute little puppy")
susi.set_conversation("Wuff, wuff!")

ricky = Friend("Ricky", "A lovely penguin")
ricky.set_conversation("Hello!")


# put characters into rooms
dining_hall.set_character(dave)
ballroom.set_character(susi)
kitchen.set_character(ricky)

current_room = kitchen

# items
cheese = Item("cheese")
old_sward = Item("old Sward")
shield = Item("Shield")
wand = Item("wand")
book = Item("Book") 

# put items in room
dining_hall.set_item(old_sward)
kitchen.set_item(shield)
ballroom.set_item(cheese)

# link items
dining_hall.link_item(old_sward)
kitchen.link_item(shield)
ballroom.link_item(cheese)

# set description of itemsi
old_sward.description = "A stump, rusty sward - let's hope you won't need it."
shield.description = "A heavy shield good to defend, but heavy to carry."
wand.description = "Wow - now you can do some magic!"
book.description = "A heavy book full of wisdom."
cheese.description = "A smelly old cheese."

old_sward.describe()

loop = True # if True room and inhabitant details are printed
while True:
    print("\n")
    if loop:
        current_room.get_details() 

        inhabitant = current_room.get_character()
        if inhabitant is not None:
            inhabitant.describe()
    
        item = current_room.get_item()
        if item is not None:
            item.describe()

    print("What do you want to do? ['talk', 'fight', set enemy to sleep, hug a friend, change the room, 'take' item]\n") 
   
    command = input("> ")
    # change room
    if command.upper().lower() in current_room.linked_rooms:
        loop = True
        current_room = current_room.move(command)
    elif command.upper().lower() in ['north', 'south', 'east', 'west']:
        loop = False
        current_room = current_room.move(command)
    # talk
    elif command.upper().lower() == "talk":
        loop = False
        if inhabitant:
            print("Talk to " + inhabitant.name + "!")
            inhabitant.talk()
        else:
            print("Sorry, there is nobody else in the room.")	
    # fight
    elif command.upper().lower() =="fight":# and isinstance(inhabitant, Enemy):
        loop = False
        if inhabitant and isinstance(inhabitant, Enemy):
            print("Fight against " + inhabitant.name + "!")
            print("What would you like to fight with?")
            combat = input("[combat item] > ") 
            if combat in backpack:
                if inhabitant.fight(combat) == True:
                    print("Yeah! You won!")
                    current_room.set_character(None)
                    loop = True
                    print(Enemy.nr_enemies)
                    if Enemy.nr_enemies == 0:
                        print("Congratulations! You defeated all Enemies!")
                        loop = False 
                        break   
                # if weapon is not weakness of inhabitant -> loose game and exit  
                else:
                    print("Oh no! You lost!")
                    break
            # check if chosen wepon is in backpack 
            elif combat not in backpack:
                print("You cannot fight with a " + combat + ". You don't have one")
        elif inhabitant and not isinstance(inhabitant, Enemy):
            print(inhabitant.name + " doesn't want to fight with you.")
        else:
            print("Sorry, there is nobody else in the room.")
    # sleep
    elif command.upper().lower() == 'sleep' and isinstance(inhabitant, Enemy):
        loop = False
        inhabitant.sleep()
    # hug
    elif command.upper().lower() == "hug" and isinstance(inhabitant, Friend):
        inhabitant.hug()
    # take 
    elif command.upper().lower() == "take" and item:
        backpack.append(item.name)
        current_room.set_item(None)
        print("Your backpack contains: {} ".format([i for i in backpack]))
        loop = False
    elif command.upper().lower() == "take":
        print("There is no item in this room") 
        loop = False
    # exit game
    elif command in ["exit", "quit"]:
        print("Awww...already leaving?") 
        break
    else:
        print("Invalid input.")
        loop = False

RPGInfo.author = "Frauke"
RPGInfo.credits()
	
