# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Giani-Wyss",  # TODO: Your Battlesnake Username
        "color": "#000000",  # TODO: Choose color
        "head": "replit-mark",  # TODO: Choose head
        "tail": "replit-notmark",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    is_move_ok = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    my_length = game_state["you"]["length"]
    my_id = game_state["you"]["id"]

    next_move_left = [my_head["x"] - 1, my_head["y"]]
    next_move_right = [my_head["x"] + 1, my_head["y"]]
    next_move_down = [my_head["x"], my_head["y"] - 1]
    next_move_up = [my_head["x"], my_head["y"] + 1]

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
        is_move_ok["left"] = False

    if my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
        is_move_ok["right"] = False

    if my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
        is_move_ok["down"] = False

    if my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False
        is_move_ok["up"] = False

    # Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width'] - 1
    board_height = game_state['board']['height'] - 1

    if my_head["x"] == 0:  # Bound is left of head, don't move left
        is_move_safe["left"] = False
        is_move_ok["left"] = False

    if my_head["x"] == board_width:  # Bound is right of head, don't move right
        is_move_safe["right"] = False
        is_move_ok["right"] = False

    if my_head["y"] == 0:  # Bound is below head, don't move down
        is_move_safe["down"] = False
        is_move_ok["down"] = False

    if my_head["y"] == board_height:  # Bound is above head, don't move up
        is_move_safe["up"] = False
        is_move_ok["up"] = False

    # Prevent your Battlesnake from colliding with itself
    # Prevent your Battlesnake from colliding with other Battlesnakes
    snakes = game_state['board']['snakes']
    
    for snake in snakes:
        for Bodypart in snake['body'][:-1]:
            Bptemp = [Bodypart["x"], Bodypart["y"]]
            if next_move_left == Bptemp:  # Body is left of head, don't move left
                is_move_safe["left"] = False
                is_move_ok["left"] = False
            
            if next_move_right == Bptemp:  # Body is right of head, don't move right
                is_move_safe["right"] = False
                is_move_ok["right"] = False

            if next_move_down == Bptemp:  # Body is below head, don't move down
                is_move_safe["down"] = False
                is_move_ok["down"] = False
    
            if next_move_up == Bptemp:  # Body is above head, don't move up
                is_move_safe["up"] = False
                is_move_ok["up"] = False

    # Choose a random move from the safe ones
    # next_move = random.choice(safe_moves)

    # Avoid Opponents next move
    op_next_move = []
    snakes_copy = []
    for snk in snakes:
        if snk['id'] != my_id:
            snakes_copy.append(snk)
        for op in snakes_copy:
            Op_head = op['head']
            op_next_move_left = [Op_head["x"] - 1, Op_head["y"]]
            op_next_move_right = [Op_head["x"] + 1, Op_head["y"]]
            op_next_move_down = [Op_head["x"], Op_head["y"] - 1]
            op_next_move_up = [Op_head["x"], Op_head["y"] + 1]
            op_next_move.append(op_next_move_left)
            op_next_move.append(op_next_move_right)
            op_next_move.append(op_next_move_down)
            op_next_move.append(op_next_move_up)
        for s in snakes_copy:
            op_length = s["length"]
            if my_length <= op_length:
                for Op_move in op_next_move:
                    if Op_move == next_move_left:
                        is_move_safe["left"] = False
                        is_move_ok["left"] = True
                    if Op_move == next_move_right:
                        is_move_safe["right"] = False
                        is_move_ok["right"] = True
                    if Op_move == next_move_down:
                        is_move_safe["down"] = False
                        is_move_ok["down"] = True
                    if Op_move == next_move_up:
                        is_move_safe["up"] = False
                        is_move_ok["up"] = True 

    # Movement decision
    safe_moves = []
    for safemove, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(safemove)

    ok_moves = []
    for okmove, isOk in is_move_ok.items():
        if isOk:
            ok_moves.append(okmove)

    food = game_state['board']['food']
    
    nearestfood = []
    distancetofood = 99
    for fooditem in food:
        tempdistancetofood = abs(fooditem["x"] - my_head["x"]) + abs(fooditem["y"] - my_head["y"])
        if tempdistancetofood < distancetofood:
            distancetofood = tempdistancetofood
            nearestfood = fooditem
   
    lowestop = []
    distancetoop = 99
    if snakes_copy == []:
        snakes_copy['head'][0] = nearestfood
    for f_op in snakes_copy:
        fight_op = f_op['head']
        tempdistancetoop = abs(fight_op["x"] - my_head["x"]) + abs(fight_op["y"] - my_head["y"])
        if tempdistancetoop < distancetoop:
            distancetoop = tempdistancetoop
            lowestop = fight_op

        for s_op in snakes_copy:
            op_length = s_op["length"]
            if my_length <= op_length:
                if len(safe_moves) != 0:
                    if my_head["x"] > nearestfood["x"] and is_move_safe["left"]:
                        next_move = "left"
                    elif my_head["x"] < nearestfood["x"] and is_move_safe["right"]:
                        next_move = "right"
                    elif my_head["y"] < nearestfood["y"] and is_move_safe["up"]:
                        next_move = "up"
                    elif my_head["y"] > nearestfood["y"] and is_move_safe["down"]:
                        next_move = "down"
                    else:
                        next_move = random.choice(safe_moves)
                elif len(ok_moves) != 0:
                    if my_head["x"] > nearestfood["x"] and is_move_ok["left"]:
                        next_move = "left"
                    elif my_head["x"] < nearestfood["x"] and is_move_ok["right"]:
                        next_move = "right"
                    elif my_head["y"] < nearestfood["y"] and is_move_ok["up"]:
                        next_move = "up"
                    elif my_head["y"] > nearestfood["y"] and is_move_ok["down"]:
                        next_move = "down"
                    else:
                        next_move = random.choice(ok_moves)
                else:
                    print(f"MOVE {game_state['turn']}: No safe moves detected!\nMoving randomly!")
                    next_move = random.choice(ok_moves)
            else:
                if len(safe_moves) != 0:
                    if my_head["x"] > lowestop["x"] and is_move_safe["left"]:
                        next_move = "left"
                    elif my_head["x"] < lowestop["x"] and is_move_safe["right"]:
                        next_move = "right"
                    elif my_head["y"] < lowestop["y"] and is_move_safe["up"]:
                        next_move = "up"
                    elif my_head["y"] > lowestop["y"] and is_move_safe["down"]:
                        next_move = "down"
                    else:
                        next_move = random.choice(safe_moves)
                elif len(ok_moves) != 0:
                    if my_head["x"] > lowestop["x"] and is_move_ok["left"]:
                        next_move = "left"
                    elif my_head["x"] < lowestop["x"] and is_move_ok["right"]:
                        next_move = "right"
                    elif my_head["y"] < lowestop["y"] and is_move_ok["up"]:
                        next_move = "up"
                    elif my_head["y"] > lowestop["y"] and is_move_ok["down"]:
                        next_move = "down"
                    else:
                        next_move = random.choice(ok_moves)
                else:
                    print(f"MOVE {game_state['turn']}: No ok moves detected!\nMoving randomly!")
                    next_move = random.choice(ok_moves)

    # Movement
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})