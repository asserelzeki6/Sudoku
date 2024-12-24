import datetime
from Backend.utils.Node import Node

def isSolvable(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                if not isValid(board, i, j, board[i][j]):
                    return False
    return True

def printBoard(board, logs):
    for i in range(9):
        print("-----------------------------------------------")
        # logs.append("-----------------------------------------------")
        for j in range(9):
            print("| ",board[i][j], end = " ")
        print(" |")
        logs.append(f"{board[i]}")
    
    print("-----------------------------------------------")
    # logs.append("-----------------------------------------------")

def BTS (assignment, board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for k in range(1,10):
                    if isValid(board, i, j, k):
                        board[i][j] = k
                        assignment[(i,j)] = k
                        if BTS(assignment,board):
                            return True
                        board[i][j] = 0
                        assignment.pop((i,j))
                return False
    return True

def isValid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num and i != col:
            return False
        if board[i][col] == num and i != row:
            return False
        if board[3*(row//3) + i//3][3*(col//3) + i%3] == num and (3*(row//3) + i//3) != row and (3*(col//3) + i%3) != col:
            return False
    return True


def generateAllArcs():
    arcs = []
    for i in range(9):
        for j in range(9):
            for neighbor in getNeighbors(i, j):
                arcs.append(((i,j),neighbor))
    return arcs

def generateAllNodes(board):
    nodes = [[None for i in range(9)] for j in range(9)]

    for i in range(9):
        for j in range(9):
            node = None
            if board[i][j] == 0:
                node = Node([1,2,3,4,5,6,7,8,9],i,j)
            else:
                node = Node([board[i][j]],i,j)
            nodes[i][j] = node
    return nodes

def ac3(nodes, arcs, logs):
    while len(arcs) != 0:
        arc = arcs.pop(0)
        if revise(nodes, arc, logs):
            if len(nodes[arc[0][0]][arc[0][1]].domain) == 0:
                return False
            for neighbor in getNeighbors(arc[0][0], arc[0][1]):
                # print(f"neighbor is {neighbor} and arc[0] is {arc[0]}")
                if neighbor != arc[1]:
                    # print("added")
                    arcs.append((neighbor, arc[0]))
    return True

def revise(nodes, arc, logs):
    revised = False
    for x in nodes[arc[0][0]][arc[0][1]].domain:
        if no_value_satisyfing_constraint(nodes, arc, x):
            # print(f"Revise: {arc[0]} {arc[1]} violation in {x} their domain is {nodes[arc[0][0]][arc[0][1]].domain} {nodes[arc[1][0]][arc[1][1]].domain}")
            logs.append(f"Revise: {arc[0]} {arc[1]} violation in {x} their domain is {nodes[arc[0][0]][arc[0][1]].domain} {nodes[arc[1][0]][arc[1][1]].domain}")
            nodes[arc[0][0]][arc[0][1]].domain.remove(x)
            # print(f"domain of i:{arc[0][0]} j:{arc[0][1]} becomes {nodes[arc[0][0]][arc[0][1]].domain}")
            logs.append(f"domain of i:{arc[0][0]} j:{arc[0][1]} becomes {nodes[arc[0][0]][arc[0][1]].domain}")
            revised = True
    return revised

def no_value_satisyfing_constraint(nodes, arc, value):
    for domain_value in nodes[arc[1][0]][arc[1][1]].domain:
        if value != domain_value:
            return False
    return True

def getNeighbors(i, j):
    neighbors = []
    for k in range(9):
        if k != j:
            neighbors.append((i,k))
        if k != i:
            neighbors.append((k,j))
    for k in range(3*(i//3), 3*(i//3) + 3):
        for l in range(3*(j//3), 3*(j//3) + 3):
            if k != i and l != j:
                neighbors.append((k,l))
    return neighbors

def backtracking_with_forward_checking(board, assignment, addLogs = False):
    logs = []
    logs.append(datetime.datetime.now())
    nodes = generateAllNodes(board)
    if isSolvable(board):
        if(backtracking(board, assignment, nodes, logs)):
            print("Solved Successfully")
            logs.append("Solved Successfully")
        else:
            print("Unsolvable")
            logs.append("Unsolvable")
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    board[i][j] = nodes[i][j].domain[0]
                    assignment[(i,j)] = nodes[i][j].domain[0]
        logs.append("-----------------------------------------------------------------------------------------")
        logs.append("Board after backtracking")
        printBoard(board, logs)
        # logs.append(board)
        logs.append("-----------------------------------------------------------------------------------------")
        logs.append("Assignment after backtracking")
        logs.append(assignment)
        if addLogs:
            writeLogs(logs)
    else:
        print("Unsolvable")

def backtracking(board, assignment, nodes, logs):
    if isComplete(nodes):
        return True
    node = selectUnassignedNode(board, nodes)
    logs.append("-----------------------------------------------------------------------------------------")
    logs.append(f"selected node is {node}")
    node.original_domain = node.domain.copy()
    for value in node.domain:
        if isValidNode(nodes, node, value):
            node.domain = [value]
            assignment[(node.i, node.j)] = value
            board[node.i][node.j] = value
            node.domain = [value]
            logs.append("-----------------------------------------------------------------------------------------")
            logs.append(f"going to the arc with i:{node.i} j:{node.j} value:{value}")
            if ac3(nodes, generateAllArcs(), logs):
                logs.append(f"PASSED AC3 with i:{node.i} j:{node.j} value:{value}")
                if backtracking(board, assignment, nodes, logs):
                    logs.append(f"PASSED BACKTRACKING with i:{node.i} j:{node.j} value:{value}")
                    return True  

            assignment.pop((node.i, node.j))
            board[node.i][node.j] = 0
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        nodes[i][j].domain = nodes[i][j].original_domain.copy()
    return False


def isComplete(nodes):
    for i in range(9):
        for j in range(9):
            if len(nodes[i][j].domain) != 1:
                return False
    return True

def selectUnassignedNode(board, nodes):
    minDomain = 10
    node = None
    for i in range(9):
        for j in range(9):
            if len(nodes[i][j].domain) > 1 and len(nodes[i][j].domain) < minDomain:
                minDomain = len(nodes[i][j].domain)
                node = nodes[i][j]
    return node

def isValidNode(nodes, node, value):
    return True

def writeLogs(logs):
    with open("logs.txt", "w") as f:
        for log in logs:
            f.write(str(log) + "\n")

def main():
    board = [
        [0,0,0 ,0,0,0 ,0,0,0],
        [0,0,0 ,0,0,3 ,0,0,0],
        [0,0,1 ,0,2,0 ,0,0,0],

        [0,0,0 ,5,0,0 ,0,0,0],
        [0,0,4 ,0,0,0 ,0,0,0],
        [0,9,0 ,0,0,0 ,0,0,0],

        [0,0,0 ,0,0,0 ,0,0,0],
        [0,0,0 ,0,0,0 ,0,0,0],
        [0,0,0 ,0,0,0 ,0,0,0]
    ]
    if isSolvable(board):
        assignment = {}
        backtracking_with_forward_checking(board, assignment, True)
        printBoard(board)
        print(assignment)
    else:
        print("Unsolvable")

if __name__ == "__main__":
    main()