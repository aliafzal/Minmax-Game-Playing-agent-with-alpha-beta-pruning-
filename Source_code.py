import random
import sys
import os
import numpy as np
import copy
import time
import random


#############################Classes##################################

class node:
    child = None
    self_grid = None
    score = None
    opp_score = None
    val = None
    move_played_c = None
    move_played_r = None

    def __init__(self):
        self.child = []
        self.self_grid = []
        self.score = 0
        self.opp_score = 0
        self.val = 0
        self.move_played_c = 'Z'
        self.move_played_r = '0'


############################Functions ################################
# dir  = 0  no left
# dir  = 1  no right
# dir  = 2  no up
# dir  = 3  no down
def find_regions(grid, check_grid, region, fruit, loc_r, loc_c, n, dir):
    if (loc_r >= 0 and loc_c >= 0 and loc_r < n and loc_c < n):
        if (check_grid[loc_r][loc_c] == False):
            if (grid[loc_r][loc_c] == fruit):
                check_grid[loc_r][loc_c] = True
                region.append([loc_r, loc_c])
                if (dir != 0):
                    find_regions(grid, check_grid, region, fruit, loc_r, loc_c - 1, n, 1)
                if (dir != 1):
                    find_regions(grid, check_grid, region, fruit, loc_r, loc_c + 1, n, 0)
                if (dir != 2):
                    find_regions(grid, check_grid, region, fruit, loc_r - 1, loc_c, n, 3)
                if (dir != 3):
                    find_regions(grid, check_grid, region, fruit, loc_r + 1, loc_c, n, 2)


def find_regions1(grid, check_grid, region, fruit, loc_r, loc_c, n, dir):
    if (loc_r >= 0 and loc_c >= 0 and loc_r < n and loc_c < n):
        if (check_grid[loc_r][loc_c] == False):
            if (grid[loc_r][loc_c] == fruit):
                check_grid[loc_r][loc_c] = True
                region.append([loc_r, loc_c])
                if (dir != 0):
                    find_regions(grid, check_grid, region, fruit, loc_r, loc_c - 1, n, 1)
                if (dir != 1):
                    find_regions(grid, check_grid, region, fruit, loc_r, loc_c + 1, n, 0)
                if (dir != 2):
                    find_regions(grid, check_grid, region, fruit, loc_r - 1, loc_c, n, 3)
                if (dir != 3):
                    find_regions(grid, check_grid, region, fruit, loc_r + 1, loc_c, n, 2)


def play_move(grid, regions):
    for i in range(regions.__len__()):
        grid[regions[i][0]][regions[i][1]] = '*'
    apply_gravity(grid, n)
    return grid


def play_move1(grid, regions, move):
    temp = copy.deepcopy(grid)
    for i in range(regions[move].__len__()):
        temp[regions[move][i][0]][regions[move][i][1]] = '*'
    apply_gravity(temp, n)
    return temp


def mergeSort(list_inp):
    if list_inp.__len__() > 1:
        mid = list_inp.__len__() // 2
        lefthf = list_inp[:mid]
        righthf = list_inp[mid:]

        mergeSort(lefthf)
        mergeSort(righthf)

        i = 0
        j = 0
        k = 0
        while i < lefthf.__len__() and j < righthf.__len__():
            if lefthf[i].__len__() > righthf[j].__len__():
                list_inp[k] = lefthf[i]
                i = i + 1
            else:
                list_inp[k] = righthf[j]
                j = j + 1
            k = k + 1

        while i < lefthf.__len__():
            list_inp[k] = lefthf[i]
            i = i + 1
            k = k + 1

        while j < righthf.__len__():
            list_inp[k] = righthf[j]
            j = j + 1
            k = k + 1




def minmax_alphabeta_max1(node1, alpha, beta, d):
    temp_grid = []
    node1.val = -sys.maxsize
    region_list = []
    if (d > -1):
        temp_grid = node1.self_grid
        check_grid = np.zeros((n, n), dtype=bool)
        region = []
        for r in range(n):
            for c in range(n):
                if (temp_grid[r][c] != '*'):
                    if (check_grid[r][c] == False):
                        check_grid[r][c] = True
                        region.append([r, c])
                        find_regions(temp_grid, check_grid, region, temp_grid[r][c], r, c + 1, n, 0)
                        find_regions(temp_grid, check_grid, region, temp_grid[r][c], r + 1, c, n, 2)
                        region_list.append(region)
                        region = []
        mergeSort(region_list)
        for ch in range(region_list.__len__()):
            child = node()
            child.move_played_c = chr(64 + region_list[ch][0][1] + 1)
            child.move_played_r = region_list[ch][0][0] + 1
            child.self_grid = copy.deepcopy(play_move1(copy.deepcopy(temp_grid), region_list, ch))
            child.score = node1.score + (region_list[ch].__len__() * region_list[ch].__len__())
            child.opp_score = node1.opp_score
            node1.child.append(child)
            node1.val = max(node1.val, minmax_alphabeta_min1(child, alpha, beta, d - 1))
            if (node1.val >= beta):
                return node1.val
            alpha = max(alpha, node1.val)

    if (region_list.__len__() <= 0):
        node1.val = node1.score - node1.opp_score
    return node1.val


def minmax_alphabeta_min1(node1, alpha, beta, d):
    temp_grid = []
    node1.val = sys.maxsize
    region_list = []

    if (d > -1):
        temp_grid = node1.self_grid
        check_grid = np.zeros((n, n), dtype=bool)
        region = []
        for r in range(n):
            for c in range(n):
                if (temp_grid[r][c] != '*'):
                    if (check_grid[r][c] == False):
                        check_grid[r][c] = True
                        region.append([r, c])
                        find_regions(temp_grid, check_grid, region, temp_grid[r][c], r, c + 1, n, 0)
                        find_regions(temp_grid, check_grid, region, temp_grid[r][c], r + 1, c, n, 2)
                        region_list.append(region)
                        region = []
        mergeSort(region_list)
        for ch in range(region_list.__len__()):
            child = node()
            child.move_played_c = chr(64 + region_list[ch][0][1] + 1)
            child.move_played_r = region_list[ch][0][0] + 1
            child.self_grid = copy.deepcopy(play_move1(copy.deepcopy(temp_grid), region_list, ch))
            child.opp_score = node1.opp_score + (region_list[ch].__len__() * region_list[ch].__len__())
            child.score = node1.score
            node1.child.append(child)
            node1.val = min(node1.val, minmax_alphabeta_max1(child, alpha, beta, d - 1))
            if (node1.val <= alpha):
                return node1.val
            beta = min(beta, node1.val)

    if (region_list.__len__() <= 0):
        node1.val = node1.score - node1.opp_score
    return node1.val


def alpha_beta_search(node1, alpha, beta, d):
    node1.val = minmax_alphabeta_max1(node1, alpha, beta, d)
    for i in range(node1.child.__len__()):
        if (node1.child[i].val == node1.val):
            return node1.child[i]



def apply_gravity(grid_data, n):
    temp_data = []
    for col in range(n):
        temp_data = grid_data[:, col]
        for f in range(temp_data.__len__()):
            if (temp_data[f] == '*'):
                temp_data = np.delete(temp_data, f)
                temp_data = np.insert(temp_data, 0, '*')
        grid_data[:, col] = temp_data


##################################### main_code_start##############

#############################Global Variables #####################
time1 = time.time()
time2 = 0
############################body#################
input = "input.txt"
input_data = []
file = open(input, "r")
# data  identification
for line in file:
    input_data.append(line)
n = int(input_data[0])
p = int(input_data[1])
t = float(input_data[2])
grid = []
for d in range(3, n + 3):
    grid.append(list(input_data[d].strip()))
m_grid = np.array(grid)
time1 = time.time()
time2 = 0
main_node = node()
play_node = node()
main_node.self_grid = m_grid

#################################################################################
region_main = []
region_list_main = []
check_grid_main = np.zeros((n, n), dtype=bool)
temp_grid_main = copy.deepcopy(m_grid)
for r in range(n):
    for c in range(n):
        if (temp_grid_main[r][c] != '*'):
            if (check_grid_main[r][c] == False):
                check_grid_main[r][c] = True
                region_main.append([r, c])
                find_regions(temp_grid_main, check_grid_main, region_main, temp_grid_main[r][c], r, c + 1, n, 0)
                find_regions(temp_grid_main, check_grid_main, region_main, temp_grid_main[r][c], r + 1, c, n, 2)
                region_list_main.append(region_main)
                region_main = []


if( t> 150 and t < 300):
    if((region_list_main.__len__() <= 100) and n > 10):
        play_node = alpha_beta_search(main_node, -sys.maxsize, sys.maxsize, 1)
    elif(n <= 10):
        play_node = alpha_beta_search(main_node, -sys.maxsize, sys.maxsize, 1)
    elif (n <= 7):
        play_node = alpha_beta_search(main_node, -sys.maxsize, sys.maxsize, 3)
    else:
        play_node = alpha_beta_search(main_node, -sys.maxsize, sys.maxsize, 0)
elif(t > 60 and t <= 150):
    if (n > 10 and region_list_main.__len__() < 65):
        play_node = alpha_beta_search(main_node, -sys.maxsize, sys.maxsize, 1)
    elif (n <= 10):
        play_node = alpha_beta_search(main_node, -sys.maxsize, sys.maxsize, 1)
    else:
        play_node = alpha_beta_search(main_node, -sys.maxsize, sys.maxsize, 0)
else:
    play_node = alpha_beta_search(main_node, -sys.maxsize, sys.maxsize, 0)

tempp = copy.deepcopy(play_node.self_grid)
file = open("output.txt", "w")
file.flush()
file.write(play_node.move_played_c)
file.write(play_node.move_played_r.__str__())
file.write('\n')
file.close()
file = open("output.txt", "a")
for a in range(tempp.__len__()):
    for b in range(tempp.__len__()):
        file.write(tempp[a][b])
    file.write('\n')
file.close()
# print(play_node.score)
# print(play_node.move_played_c, end='', flush=True)
# print(play_node.move_played_r)
#
# time2 = time.time()
# print(time2 - time1)
# print(t)