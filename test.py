# coding=utf-8
'''
File Header：
@Author: Chuhuan Huang
Contacts: chh172@ucsd.edu/ chuhuan1118@163.com/ chuhuanh@usc.edu
Description:
This file covers the most of unit-testing and overall simulations
'''

from graph import *
import sys
import numpy as np

sys.setrecursionlimit(1000)


def test_prob():
    # here we test out state transition function aka prob
    # note that classification of state transition corresponds to action
    # beyond the action, we need test several impossible state transition serve as boundary cases

    # a = 1/ start

    # print(prob((1, 0, 0), (0, 0, 0), 1) == 0.82)
    # print(prob((2, 0, 0), (0, 0, 0), 1) == 0.17)
    # print(prob((3, 0, 0), (0, 0, 0), 1) == 0.01)

    # a = 2/ 平A
    # todo: 平A under no protection : 1、2、3、-1、-2 / 平A after a protection or protections

    print(prob((4, 0, 0), (3, 0, 0), 2) == 0.2 * 0.82)
    print(prob((5, 0, 0), (3, 0, 0), 2) == 0.2 * 0.17)
    print(prob((6, 0, 0), (3, 0, 0), 2) == 0.2 * 0.01)

    print(prob((-1, 0, 1), (1, 0, 0), 2) == 0.8 * 0.25)
    print(prob((0, 0, 1), (2, 0, 0), 2) == 0.8 * 0.25)
    print(prob((2, 0, 1), (3, 0, 0), 2) == 0.8 * 0.75)

    # 平A after a protection or protections

    # print(prob((6, 0, 0), (3, 2, 0), 2) == 0.2 * 0.01)
    # print(prob((4, 0, 0), (3, 1, 0), 2) == 0.2 * 0.82)
    # print(prob((4, 0, 0), (2, 2, 0), 2) == 0.2 * 0.17)

    # a = 3/ 保护追加
    # print(prob((6, 0, 0), (3, 2, 0), 3) == 0.01)
    # print(prob((6, 0, 0), (3, 1, 0), 3) == 0.2 * 0.01)
    # print(prob((6, 0, 0), (4, 2, 0), 3) == 0.17)
    # print(prob((9, 0, 0), (6, 2, 0), 3) == 0.01)
    # print(prob((8, 0, 0), (5, 0, 0), 3) == 0.2 * 0.01)
    # print(prob((3, 2, 0), (3, 1, 0), 3) == 0.8)
    # print(prob((3, 1, 0), (3, 0, 0), 3) == 0.8)
    # a = 4/ 领取奖励结束本轮并回到原点

    # print(prob((-1, 0, 1), (0, 0, 0), 4) == 0)

    # boundary case
    # print(prob((2, 0, 0), (3, 0, 0), 2) == 0)
    # print(prob((8, 0, 0), (3, 0, 0), 2) == 0)
    # print(prob((-1, 0, 1), (9, 0, 0), 4) == 0)
    # print(prob((8, 0, 0), (4, 2, 0), 3) == 0)
    # print(prob((2, 0, 0), (0, 0, 0), 3) == 0)
    # print(prob((2, 0, 0), (8, 0, 0), 3) == 0)
    # print(prob((0, 0, 0), (0, 0, 0), 4) == 0)
    # print(prob((3, 2, 0), (3, 0, 0), 3) == 0)
    return


def test_rewards():
    build_tree()
    generate_all_trajectory()
    # for n in T_ARR[634]:
    #     print n.get_state()
    print(len(T_ARR))
    print(len(T_ARR[13245]))
    print_trajectory(T_ARR[13245])
    calculator(T_ARR[13245])

    for t in T_ARR:
        for n in t:
            if n.get_state()[1] > 0:
                print(n.get_state())
    count = 0
    for T in T_ARR:
        if calculator(T) > 0:
            count = count + 1
    print(count)

    return


def test_policy():
    print(policy((0, 0, 0)))
    print(q((0, 0, 0), 1))
    # for s in S:
    #     print(s, Value[s], policy(s))
    # return


def random_state_generator(s, a):
    Buffer = []
    Prob_dist = []
    for sp in S:
        if prob(sp, s, a) != 0:
            Buffer.append(Node(sp))
            Prob_dist.append(prob(sp, s, a))

    if len(Buffer) != 0:
        return np.random.choice(Buffer, 1, p=Prob_dist)[0].get_state()


def simulation(iterations):
    R = 0
    # for i in range(1, 1001):
    for i in range(iterations):
        s = (0, 0, 0)
        a = policy(s)
        sp = random_state_generator(s, a)
        R = R + rewards(sp, s, a)
        # print(sp, s, a)
        while sp != (0, 0, 0):
            s = sp
            a = policy(s)
            sp = random_state_generator(s, a)
            # print(sp, s, a)
            R = R + rewards(sp, s, a)
    print(R / k, "learned_policy")
    return


def all_random_policy(s):
    if s not in S:
        return
    if s == (0, 0, 0):
        return 1
    elif s[0] >= 7 or s[2] == 1:
        return 4
    else:
        return np.random.choice([2, 3, 4], 1)[0]


def simulation_all_random_policy(iterations):
    R = 0
    # for i in range(1, 1001):
    for i in range(iterations):
        s = (0, 0, 0)
        a = all_random_policy(s)
        sp = random_state_generator(s, a)
        R = R + rewards(sp, s, a)
        # print(sp, s, a)
        while sp != (0, 0, 0):
            s = sp
            a = all_random_policy(s)
            sp = random_state_generator(s, a)
            # print(sp, s, a)
            R = R + rewards(sp, s, a)
        # print(R)
    print(R / k, "all_random_policy")
    return


# 四星平A
def chh_policy_1(s):
    if s not in S:
        return
    if s == (0, 0, 0):
        return 1
    elif s[0] >= 6 or s[2] == 1:
        return 4
    elif s[0] == 2 or s[0] == 3:
        return 3
    else:
        return 2


# 四星领取
def chh_policy_2(s):
    if s not in S:
        return
    if s == (0, 0, 0):
        return 1
    elif s[0] >= 6 or s[2] == 1 or s[0] == 4:
        return 4
    elif s[0] == 2 or s[0] == 3:
        return 3
    else:
        return 2


def simulation_chh_policy_1(iterations):
    R = 0
    # for i in range(1, 1001):
    for i in range(iterations):
        s = (0, 0, 0)
        a = chh_policy_1(s)
        sp = random_state_generator(s, a)
        R = R + rewards(sp, s, a)
        # print(sp, s, a)
        while sp != (0, 0, 0):
            s = sp
            a = chh_policy_1(s)
            sp = random_state_generator(s, a)
            # print(sp, s, a)
            R = R + rewards(sp, s, a)
        # print(R)
    print(R / k, "chh_policy_1")
    return


def simulation_chh_policy_2(iterations):
    R = 0
    # for i in range(1, 1001):
    for i in range(iterations):
        s = (0, 0, 0)
        a = chh_policy_2(s)
        sp = random_state_generator(s, a)
        R = R + rewards(sp, s, a)
        # print(sp, s, a)
        while sp != (0, 0, 0):
            s = sp
            a = chh_policy_2(s)
            sp = random_state_generator(s, a)
            # print(sp, s, a)
            R = R + rewards(sp, s, a)
        # print(R)
    print(R / k, "chh_policy_2")
    return


# test_prob()
# test_rewards()
test_policy()
k = 100000
# simulation(k)
# simulation_all_random_policy(k)
# simulation_chh_policy_1(k)
# simulation_chh_policy_2(k)
