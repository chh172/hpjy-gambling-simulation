# coding=utf-8
'''
File Header：
@Author: Chuhuan Huang
Contacts: chh172@ucsd.edu/ chuhuan1118@163.com/ chuhuanh@usc.edu
Description:
This file creates several functions and a class useful for the test_rewards / simulations
An intuitive thinking of test rewards function is to generate all possible trajectories and calculate their total
rewards respectively. Thus, I applied a generic tree as the structure for holding all possible trajectories
'''

from hpjy import *


Tree = []
# the body of the Tree
G = []
# grandson node, lowest level node
T_ARR = []
# the list that contains all possible trajectory


class Node:
    def __init__(self, state, parent=None, children=None, action=None):
        """

        :rtype: object
        """
        self.state = state
        # state
        self.children = children
        # list of child Node
        self.parent = parent
        # parent Node
        self.action = action
        # action that brings from parent state to child state
        # here we define a None action a == 0 for root state

    def add_child(self, child):
        self.children.append(child)

    def get_state(self):
        return self.state

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def get_action(self):
        return self.action


def build_tree():
    dfs_build(Node((0, 0, 0), None, [], 0))
    return


# recursive helper function to build the generic family tree
# source is a node we traverse from
def dfs_build(source):
    Tree.append(source)
    # base case
    if source.get_state()[0] > 6 or source.get_state()[2] == 1:
        G.append(source)
        return
    # inductive step
    for sp in S:
        for a in A:
            if prob(sp, source.get_state(), a) > 0 and sp != (0, 0, 0):
                source.add_child(Node(sp, source, [], a))
    for child in source.get_children():
        dfs_build(child)


# this function build a trajectory that originates from origin to grandson
def generate_trajectory(grandson):
    T = []
    i = grandson
    T.append(grandson)
    while i.get_parent() is not None:
        T.append(i.get_action())
        i = i.get_parent()
        T.append(i)
    T.reverse()
    T.append(4)
    T.append(Node((0, 0, 0), grandson, [], 4))
    # action 4 brings grandson back to origin for next round of the game
    return T


# create the list of all trajectory
def generate_all_trajectory():
    for g in G:
        T_ARR.append(generate_trajectory(g))


# print the trajectory
def print_trajectory(T):
    for n in T:
        if n in A:
            print(n)
        else:
            print(n.get_state())


# calculate the total reward of a given trajectory
# input variable is the given trajectory, a List which connects Nodes and actions in series
# output is a real number representing the total reward of this given trajectory
def calculator(T):
    M = 0.00
    for t in T:
        if t == T[len(T) - 1]:
            break
        if t not in A:
            M = M + rewards(T[T.index(t) + 2].get_state(), t.get_state(), T[T.index(t) + 1])

    return M
