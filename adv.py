from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# WRITE STUFF HERE
# BFT can't just be used, although it can be used to find rooms that haven't been visited
# Have to build graph on the fly, each room you can know that it has exits, just not what room they lead to
# ie you know that the edges exist to go somewhere, just not where
# If there's a question mark (?), you can choose to go in a direction usign the player.travel function
# As you travel, you can build up your path that you've gone, so that maybe you can navigate back to 
# an area that has ? as options, so if you hit a dead end, go back to where the last question mark was
# Start with DFT
# Then use BFS to find rooms with ? if you get stuck
# Will need to take the slowly built up graph and use it to navigate. BFS will return a bunch of room IDs, 
# but you'll then need to use those to navigate back to a room with a ?
# While navigating again, you'll need to add the directions you navigate to your traversal path


# 1) Build new graph variable that stores a room, its exits, and where the exits lead
# The exits initially will lead to question marks, we'll update these and fill them in as we go along
# 2) Build a travel function that operates as long as the number of rooms is less than the known 
# number of room on the map. Basically a while loop, but most likely a depth-first traversal.
# 2a) This loop has to have logic that allows you to hit a dead end and then probably run a breadth 
# first traversal to make your way back to the nearest room with unknown exits. So this BFS needs to 
# return that path to the room (which will just be the room numbers)
# 2b) Once you know the rooms, you need to produce a path for the player to navigate to that room
# and then have them start the traversal function again

known_rooms = {}

while len(known_rooms) < len(room_graph):
    # log current room and exits
    current_room = player.current_room
    known_rooms[current_room.id] = {i:'?' for i in current_room.get_exits()}
    # if all points are known, we'll have to do a BFS, but that comes later
    # Create a list of directions that have an unknown next room
    unknown_directions = [i for i in known_rooms[current_room.id] if known_rooms[current_room.id][i] == '?']
    # Randomly choose from useful options
    choice = random.choice(unknown_directions)
    # Add to our traversal path
    traversal_path.append(choice)
    # Move the player
    player.travel(choice)
    # add the room to the direction, overwriting the '?'
    new_room = player.current_room.id
    known_rooms[current_room.id][choice] = new_room

print(known_rooms)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
