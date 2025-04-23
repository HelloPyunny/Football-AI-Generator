# node_pool.py

"""
node_pool.py

consider all positions in a soccer field and consider them a node
we will import this file for other files as (from node_pool import ALL_NODES)

there is a concept called 'line' here that represents literally the line in a soccer field

line 0 = Goalkeeper line | includes: GK
line 1 = Defender line | includes: LB, LCB, CB, RCB, RB
line 2 = Center Defending Midfielder/Attacking Wing Back line | includes: LDM, CDM, RDM
line 3 = Midfielder line | includes: LM LCM CM RCM RM
line 4 = Attacking Midfielder and Wings | includes: LW LAM CAM RAM RW
line 5 = Striker line | includes: LST ST RST

and 'desc' is just a description :)
"""
ALL_NODES = {
    # line 0 = Goalkeeper line | includes: GK
    "GK": {"line": 0, "desc": "Goalkeeper"},
    
    # line 1 = Defender line | includes: LB, LCB, CB, RCB, RB
    "LB":    {"line": 1, "desc": "Left Back"},
    "CB":    {"line": 1, "desc": "Center Back"},
    "RB":    {"line": 1, "desc": "Right Back"},

    # line 2 = Center Defending Midfielder/Attacking Wing Back line | includes: LDM, CDM, RDM
    "CDM":   {"line": 2, "desc": "Center Defensive Midfielder"},

    # line 3 = Midfielder line | includes: LM LCM CM RCM RM
    "LM":    {"line": 3, "desc": "Left Midfielder"},
    "CM":    {"line": 3, "desc": "Center Midfielder"},
    "RM":    {"line": 3, "desc": "Right Midfielder"},

    # line 4 = Attacking Midfielder and Wings | includes: LW LAM CAM RAM RW
    "LW":    {"line": 3, "desc": "Left Winger"},
    "CAM":   {"line": 3, "desc": "Center Attacking Midfielder"},
    "RW":    {"line": 3, "desc": "Right Winger"},

    # line 5 = Striker line | includes: LST ST RST
    "ST":    {"line": 4, "desc": "Striker"},
}