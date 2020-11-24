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

opposite_direction = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

# def bfs(self, starting_vertex, destination_vertex):
#     q = Queue()
#     visited = set()
#     q.enqueue([starting_vertex])

#     while q.size() > 0:
#         current_path = q.dequeue()
#         current_node = current_path[-1]
#     ​
#     if current_node == destination_vertex:
#         return current_path
#     ​
#     if current_node not in visited:
#         visited.add(current_node)

#     neighbors = self.get_neighbors(current_node)
#     for neighbor in neighbors:
#         # path_copy = list(current_path)
#         # path_copy = current_path.copy()
#         # path_copy = copy.copy(current_path)
#         # path_copy = current_path[:]
#     ​
#     # path_copy.append(neighbor)
#     path_copy = current_path + [neighbor]


def has_unknown_rooms(room):
    unknown_directions = [i for i in known_rooms[room.id]
                          if known_rooms[room.id][i] == '?']
    return unknown_directions

# Start by building out the graph for the first item
known_rooms[player.current_room.id] = {i: '?' for i in player.current_room.get_exits()}

# movement_history = Stack()
movement_history = []


while len(known_rooms) < len(room_graph):
    # Create a list of directions that have an unknown next room
    unknown_directions = has_unknown_rooms(player.current_room)
    # If there are no unknown directions, we need to do a BFS
    # Create stack as I move/travel
    # If I get stuck/no exits, move backwards through the stack 
    # at each room, evaluate whether there are ? exits
    # then continue
    
    # Let's try backtracking instead of BFS initially
    if len(unknown_directions) == 0:
        while len(has_unknown_rooms(player.current_room)) == 0:
            #
            backtrack = movement_history.pop()
            traversal_path.append(opposite_direction[backtrack])
            player.travel(opposite_direction[backtrack])
            # Update unknown_directions
            unknown_directions = has_unknown_rooms(player.current_room)
            
        # continue

    # Try this later
    # if len(unknown_directions) == 0:
    #     # BFS baby
    #     q = Queue()
    #     visited = set()
    #     q.enqueue(player.current_room)
    #     while q > 0:
    #         current = q.dequeue()
    #         # if the current item has rooms == ?, then let's go!
    #         if has_unknown_rooms(current) > 0:
    #             return current
    #         if current not in visited:
    #             visited.add(current)
    #         directions = player.current_room.get_exits()
    #         for direction in directions:
    #             if direction not in visited:
    #                 visited[direction] = direction
    #                 q.enqueue()

    # Randomly choose from useful options
    choice = random.choice(unknown_directions)
    # Add to our traversal and history paths
    traversal_path.append(choice)
    movement_history.append(choice)
    # Set previous room
    prev_room = player.current_room
    # Move the player
    player.travel(choice)
    # add the room to the direction, overwriting the '?'
    new_room = player.current_room
    # Update the previous room to update what room we ended up in
    known_rooms[prev_room.id][choice] = new_room.id
    # Add new room to graph
    if player.current_room.id not in known_rooms:
        known_rooms[player.current_room.id] = {i: '?' for i in player.current_room.get_exits()}
    # Update new room to represent what room we came from
    known_rooms[player.current_room.id][opposite_direction[choice]] = prev_room.id

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
