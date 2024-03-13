# Convert from the target direction to a corresponding move in the map
#


def dir_to_move(dir):
    directions = {
        "N": [1, 0],
        "NE": [1, 1],
        "E": [0, 1],
        "SE": [-1, 1],
        "S": [-1, 0],
        "SW": [-1, -1],
        "W": [0, -1],
        "NW": [1, -1],
    }

    return directions.get(dir, [0, 0])


# Example usage
if __name__ == "__main__":
    direction = "N"
    move_vector = dir_to_move(direction)
    print(move_vector)
