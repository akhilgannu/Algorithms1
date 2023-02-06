import sys
sys.setrecursionlimit(100000)

# Reading command-line arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# Reading input as lines
with open(input_file, 'r') as f:
    lines = f.readlines()


# Transforming input to adjacency matrix
def create_adj_matrix():
    """
    Creates adjacency matrix from the given input file
    :return: tuple of grid, rows, and cols
    """
    rs = 0
    cs = 0
    mat = []
    line_count = 0
    for line in lines:
        line_count += 1
        if line_count == 1:
            dimensions = line.split(' ')
            rs = int(dimensions[0])
            cs = int(dimensions[1])
        else:
            row = line.split(' ')
            row[cs - 1] = row[cs - 1].rstrip()
            mat.append(row)
    return mat, rs, cs


grid, rows, cols = create_adj_matrix()

# Transposing matrix to align with rows and columns (needs only when graph is not NxN)
grid = [*zip(*grid)]

# Directions to moving pointers
moves = {"N": (0, -1),
         "S": (0, 1),
         "E": (1, 0),
         "W": (-1, 0),
         "NE": (1, -1),
         "NW": (-1, -1),
         "SE": (1, 1),
         "SW": (-1, 1)}

# Visited nodes tracker
visited = set()


# Depth first to check for path existence
def graph_traversal(r, c, output):
    """
    Depth First Search graph traversal algorithm with modified conditions
    :param r: row index
    :param c: column index
    :param output: current output path
    :return: none
    """
    # update output file when bottom-right corner hits
    if r == (rows - 1) and c == (cols - 1):
        output = output.lstrip()  # removes a leading whitespace
        opf = open(output_file, "w")
        opf.write(output)
        opf.close()
        exit(1)

    # combining row and column index to check if visited already
    node_pointer = str(r) + "" + str(c)
    if node_pointer in visited:
        return

    # update visited set
    visited.add(node_pointer)

    # extract node's properties
    node = grid[r][c].split('-')
    node_color = node[0]
    node_direction = node[1]

    # Iterate over directional neighbors
    steps = 0
    while True:
        steps += 1
        # update row and column based on node direction to move next
        r += moves[node_direction][0]
        c += moves[node_direction][1]
        if 0 <= r < rows and 0 <= c < cols:
            next_node = grid[r][c].split('-')
            # check for the paths from opposite colored neighbor
            if next_node[0] != node_color:
                graph_traversal(r, c, output + " {}{}".format(steps, node_direction))
        # out of grid bounds
        else:
            break


if __name__ == '__main__':
    # Start of the algorithm at top-left corner (i: 0, j: 0) with empty path
    graph_traversal(0, 0, "")
