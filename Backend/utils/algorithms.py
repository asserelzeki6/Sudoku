import datetime
from Backend.utils.Node import Node
# from Node import Node

def LCV (board, node):
    lcv = []
    conflict_map = {i: 0 for i in node.domain}
    for i in node.domain:
        for neighbour in getNeighbors(node.i, node.j):
            if board[neighbour[0]][neighbour[1]] == 0:
                for j in range(9):
                    if board[neighbour[0]][j] == 0:
                        if i in node.domain:
                            conflict_map[i] += 1
                    if board[j][neighbour[1]] == 0:
                        if i in node.domain:
                            conflict_map[i] += 1
                for j in range(3*(neighbour[0]//3), 3*(neighbour[0]//3) + 3):
                    for k in range(3*(neighbour[1]//3), 3*(neighbour[1]//3) + 3):
                        if board[j][k] == 0:
                            if i in node.domain:
                                conflict_map[i] += 1
    lcv = sorted(conflict_map, key=conflict_map.get)
    return lcv
    

def isSolvable(board):
    # for i in range(9):
    #     for j in range(9):
    #         if board[i][j] != 0:
    #             if not isValid(board, i, j, board[i][j]):
    #                 return False
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
                    # print(f"i:{i} j:{j} k:{k}")
                    if isValid(board, i, j, k):
                        # print(f"valid")
                        board[i][j] = k
                        assignment[(i,j)] = k
                        if BTS(assignment,board):
                            return True
                        board[i][j] = 0
                        assignment.pop((i,j))
                return False
    return True

# def isValid(board, row, col, num):
#     for i in range(9):
#         if board[row][i] == num and i != col:
#             return False
#         if board[i][col] == num and i != row:
#             return False
#         if board[3*(row//3) + i//3][3*(col//3) + i%3] == num and (3*(row//3) + i//3) != row and (3*(col//3) + i%3) != col:
#             return False
#     return True
def isValid(self, row, col, num):
        if num in self.board[row]:
            return False
        if num in [self.board[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

# def isValid(board, row, col, num):
#         if num in board[row]:
#             return False
#         if num in [board[i][col] for i in range(9)]:
#             return False
#         start_row, start_col = 3 * (row // 3), 3 * (col // 3)
#         for i in range(start_row, start_row + 3):
#             for j in range(start_col, start_col + 3):
#                 if board[i][j] == num:
#                     return False
#         return True

# def isValid(board, i, j, val):
#     # Check the row
#     for col in range(9):
#         if board[i][col] == val:
#             return False

#     # Check the column
#     for row in range(9):
#         if board[row][j] == val:
#             return False

#     # Check the 3x3 sub-grid
#     subgrid_row_start = 3 * (i // 3)
#     subgrid_col_start = 3 * (j // 3)
#     for row in range(subgrid_row_start, subgrid_row_start + 3):
#         for col in range(subgrid_col_start, subgrid_col_start + 3):
#             if board[row][col] == val:
#                 return False

#     # If no conflict, return True
#     return True


# def isValid(board, row, col, num):
#     for i in range(9):
#         if board[row][i] == num and i != col:
#             return False
#         if board[i][col] == num and i != row:
#             return False
#         if board[3*(row//3) + i//3][3*(col//3) + i%3] == num and (3*(row//3) + i//3) != row and (3*(col//3) + i%3) != col:
#             return False
#     return True

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
                if neighbor != arc[1] :
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
    logs.append("-----------------------------------------------------------------------------------------")
    logs.append("Board before solution")
    print("Board before solution")
    printBoard(board, logs)
    if isSolvable(board):
        if(backtracking(board, assignment, nodes, logs)):
            print("Solved Successfully")
            logs.append("Solved Successfully")
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        board[i][j] = nodes[i][j].domain[0]
                        assignment[(i,j)] = nodes[i][j].domain[0]
        else:
            print("Unsolvable from backtracking")
            logs.append("Unsolvable")
            if addLogs:
                writeLogs(logs)
            return False
        
        logs.append("-----------------------------------------------------------------------------------------")
        logs.append("Board after solution")
        print("Board after solution")
        printBoard(board, logs)
        # logs.append(board)
        logs.append("-----------------------------------------------------------------------------------------")
        logs.append("Assignment after backtracking")
        logs.append(assignment)
        if addLogs:
            writeLogs(logs)

        return True
    
    else:
        print("Unsolvable")
        return False

def backtracking(board, assignment, nodes, logs):
    if isComplete(nodes):
        return True
    node = MRV(board, nodes)
    if node is None:
        return False
    logs.append("-----------------------------------------------------------------------------------------")
    logs.append(f"selected node is {node}")
    for value in LCV(board, node):
        if isValidNode(nodes, node, value):
            # for i in range(9):
            #     for j in range(9):
            #         # print(f"i:{i} j:{j} board[i][j]:{board[i][j]}")
            #         if board[i][j] == 0:
            #             nodes[i][j].original_domain = nodes[i][j].domain.copy()
            #         logs.append(f"before i:{i} j:{j} board[i][j]:{nodes[i][j].domain} and original domain is {nodes[i][j].original_domain}")
            original_domains = [[nodes[i][j].domain.copy() for j in range(9)] for i in range(9)]
            logs.append(f"before backtracking i:{i} j:{j} domain is {original_domains[i][j]}")

            assignment[(node.i, node.j)] = value
            board[node.i][node.j] = value
            node.domain = [value]
            logs.append("-----------------------------------------------------------------------------------------")
            logs.append(f"going to the arc with i:{node.i} j:{node.j} value:{value} and domain is {node.domain}")
            if ac3(nodes, generateAllArcs(), logs):
                logs.append(f"PASSED AC3 with i:{node.i} j:{node.j} value:{value}")
                if backtracking(board, assignment, nodes, logs):
                    logs.append(f"PASSED BACKTRACKING with i:{node.i} j:{node.j} value:{value}")
                    return True  

            assignment.pop((node.i, node.j))
            board[node.i][node.j] = 0
            logs.append("-----------------------------------------------------------------------------------------")
            logs.append(f"FAILED BACKTRACKING with i:{node.i} j:{node.j} value:{value}")
            for i in range(9):
                for j in range(9):
                    nodes[i][j].domain = original_domains[i][j]
                    logs.append(f"after backtracking failure i:{i} j:{j} domain becomes {original_domains[i][j]}")
            logs.append("-----------------------------------------------------------------------------------------")
        else:
            logs.append(f"NON VALID : FAILED BACKTRACKING with i:{node.i} j:{node.j} value:{value}")
    return False


def isComplete(nodes):
    for i in range(9):
        for j in range(9):
            if len(nodes[i][j].domain) != 1:
                return False
    return True

def MRV(board, nodes):
    minDomain = 10
    node = None
    for i in range(9):
        for j in range(9):
            # if board[i][j] len(nodes[i][j].domain) > 1 and len(nodes[i][j].domain) < minDomain:
            if board[i][j]==0 and len(nodes[i][j].domain) < minDomain:
                # return nodes[i][j]
                if len(nodes[i][j].domain) == minDomain:
                    lcv1 = LCV(board, node)
                    lcv2 = LCV(board, nodes[i][j])
                    if lcv1[0] > lcv2[0]:
                        minDomain = len(nodes[i][j].domain)
                        node = nodes[i][j]
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
    board = [ [7, 0, 0,  0, 0, 0,  0, 0, 6],
              [0, 0, 0,  0, 1, 0,  5, 8, 9],
              [0, 0, 0,  0, 2, 4,  0, 0, 0],

              [4, 0, 5,  0, 0, 0,  9, 0, 0],
              [0, 1, 3,  0, 6, 0,  0, 0, 0],
              [0, 0, 0,  0, 0, 7,  8, 5, 0],

              [0, 0, 0,  0, 0, 6,  0, 0, 0],
              [3, 0, 6,  0, 0, 5,  2, 0, 0],
              [5, 2, 0,  0, 9, 0,  0, 0, 8]]
    
    # board = [ [7, 0, 0, 3, 0, 4, 9, 0, 0],
    #           [0, 0, 0, 0, 9, 0, 0, 2, 0],
    #           [0, 0, 0, 0, 0, 0, 4, 0, 7],
    #           [0, 0, 0, 0, 0, 7, 0, 0, 0],
    #           [0, 6, 0, 0, 3, 0, 0, 9, 1],
    #           [0, 0, 2, 5, 4, 0, 0, 0, 0],
    #           [0, 0, 6, 0, 0, 0, 1, 0, 0],
    #           [4, 0, 0, 2, 1, 0, 5, 3, 0],
    #           [0, 0, 3, 0, 0, 6, 0, 4, 0]]
    if isSolvable(board):
        assignment = {}
        if(backtracking_with_forward_checking(board, assignment, True)):
        # if(BTS(assignment, board)):
            print("Solved Successfully")
            # for i in range(9):
            #     print(board[i])
        else:
            print("Unsolvable from main awy")
        # printBoard(board)
        # print(assignment)
    else:
        print("Unsolvable")

if __name__ == "__main__":
    main()

#  [7, 0, 0,  0, 0, 0,  0, 0, 6]
#  [0, 0, 0,  0, 1, 0,  5, 8, 9]
#  [0, 0, 0,  0, 2, 4,  0, 0, 0]

#  [4, 0, 5,  0, 0, 0,  9, 0, 0]
#  [0, 1, 3,  0, 6, 0,  0, 0, 0]
#  [0, 0, 0,  0, 0, 7,  8, 5, 0]

#  [0, 0, 0,  0, 0, 6,  0, 0, 0]
#  [3, 0, 6,  0, 0, 5,  2, 0, 0]
#  [5, 2, 0,  0, 9, 0,  0, 0, 8]

#    0 1 2 3 4 5 6 7 8
 ###################   
# 0  7 3 1 9 5 8 4 2 6
# 1  6 4 2 7 1 3 5 8 9
# 2  9 5 8 6 2 4 1 3 7
# 3  4 7 5 1 8 2 9 6 3
# 4  8 1 3 5 6 9 7 4 2
# 5  2 6 9 4 3 7 8 5 1
# 6  1 8 7 2 4 6 3 9 5
# 7  3 9 6 8 7 5 2 1 4
# 8  5 2 4 3 9 1 6 7 8