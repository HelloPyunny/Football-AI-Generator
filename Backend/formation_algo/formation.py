# formation.py

from .node_pool import ALL_NODES

# set line as list by formations
# [ ] is line, and in each line node(position) goes in

FORMATIONS = {
    # 442
    "442": {
        "lines": [
            ["GK"],
            ["LB", "CB", "CB", "RB"],
            ["LM", "CM", "CM", "RM"],
            ["ST", "ST"]
        ]
    },
    # 433 (정석)
    "433 (정석)": {
        "lines": [
            ["GK"],
            ["LB", "CB", "CB", "RB"],
            ["CM", "CM", "CM"],
            ["LW", "RW"],
            ["ST"]
        ]
    },
    # 433 (원볼란치)
    "433 (원볼란치)": {
        "lines": [
            ["GK"],
            ["LB", "CB", "CB", "RB"],
            ["CDM"],
            ["CM", "CM"],
            ["LW", "RW"],
            ["ST"]
        ]
    },
    # 4231
    "4231": {
        "lines": [
            ["GK"],
            ["LB", "CB", "CB", "RB"],
            ["CDM", "CDM"],
            ["CAM"],
            ["LW", "RW"],
            ["ST"]
        ]
    },
    # 352
    "352": {
        "lines": [
            ["GK"],
            ["CB", "CB", "CB"],
            ["CDM"],
            ["LB", "CM", "CM", "RB"],
            ["ST", "ST"]
        ]
    },
    # 343
    "343": {
        "lines": [
            ["GK"],
            ["CB", "CB", "CB"],
            ["LB", "CM", "CM", "RB"],
            ["LW", "RW"],
            ["ST"]
        ]
    },
    # 532
    "532": {
        "lines": [
            ["GK"],
            ["LB", "CB", "CB", "CB", "RB"],
            ["CM", "CM", "CM"],
            ["ST", "ST"]
        ]
    },
    # 541
    "541": {
        "lines": [
            ["GK"],
            ["LB", "CB", "CB", "CB", "RB"],
            ["LM", "CM", "CM", "RM"],
            ["ST"]
        ]
    },
    # 4141
    "4141": {
        "lines": [
            ["GK"],
            ["LB", "CB", "CB", "RB"],
            ["CDM"],
            ["LM", "CM", "CM", "RM"],
            ["ST"]
        ]
    },
    # 4222
    "4222": {
        "lines": [
            ["GK"],
            ["LB", "CB", "CB", "RB"],
            ["CDM", "CDM"],
            ["CM", "CM"],
            ["ST", "ST"]
        ]
    },
    # 4312
    "4312": {
        "lines": [
            ["GK"],
            ["LB", "CB", "CB", "RB"],
            ["CDM"],
            ["CM", "CM"],
            ["CAM"],
            ["ST", "ST"]
        ]
    }
}

def get_flat_node_list(formation_name):
    """
    return 1D list by the given formation_name
    ex) "442" -> ['GK', 'LB', 'LCB', 'RCB', 'RB', 'LM', 'LCM', 'RCM', 'RM', 'LST', 'RST']
    """
    formation = FORMATIONS.get(formation_name)
    if formation is None:
        raise ValueError(f"Formation '{formation_name} is not defined.")
    flat_list = []
    for line in formation["lines"]:
        flat_list.extend(line)
    return flat_list

def get_line_info(formation_name):
    """
    return node(position) list by the given formation_name
    """
    formation = FORMATIONS.get(formation_name)
    if formation is None:
        raise ValueError(f"Formation '{formation_name} is not defined.")
    return formation["lines"]

if __name__ == "__main__":
    for name in FORMATIONS:
        print(f"formation: {name}")
        print("  flat node list:", get_flat_node_list(name))
        print("  line composition:")
        for idx, line in enumerate(get_line_info(name), start=1):
            # can also print the descriptions by each line with formation
            line_info0 = [f"{pos} ({ALL_NODES[pos]['desc']})" for pos in line]
            print(f"    line {idx}: {line_info0}")
        print("-" * 50)