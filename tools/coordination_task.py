#!/usr/bin/env python
# coding: utf-8

import numpy as np
import random
from mutualModelling import model,agent
import matplotlib.pyplot as plt
import copy

def create_teacher(name,all_names):
    percepts = ["success","fail"]
    #actions = ["a","b","c","reward","punish"]
    actions = ["a","b","c","reward","punish"]
    rewards = [["success",1.,1.]]
    teacher = agent.Agent(name,all_names,percepts,actions,rewards)
    return teacher

def create_learner(name,all_names):
    percepts = ["reward"]
    actions = ["a","b","c","imitate"]
    #rewards = []
    rewards = [["reward",1.,1.],["punish",1.,-1]]
    learner = agent.Agent(name,all_names,percepts,actions,rewards)
    return learner


"""
"""

# parameters

name1 = "teacher"
name2 = "learner"
all_names = [name1,name2]

N = 20
n = 3000
CUMREW = np.zeros(n)

def world_update(action1,action2,previous):
    if action2 =="imitate":
        action2 = action1
    p1 = [(action2,1.)]
    p2 = [(action1,1.)]
    r = 0
    if "a"==action2:
        p1.append(("success",1.))
        #p2.append(("success",1.))
        r = 1
    else:
        p1.append(("fail",1.))
        #p2.append(("fail",1.))

    # suppose no errors of perception:

    #model_percepts1 = {name1:p1}#,name2:p2,name2+";"+name1:p1}
    #model_percepts2 = {name2:p2}#,name1:p1,name1+";"+name2:p2}
    model_percepts1 = {name1:p1,name2:p2}#,name2+";"+name1:p1}
    model_percepts2 = {name2:p2,name1:p1}#,name1+";"+name2:p2}
    #model_percepts1 = {name1:p1,name2:p2,name2+";"+name1:p1}
    #model_percepts2 = {name2:p2,name1:p1,name1+";"+name2:p2}

    return model_percepts1,model_percepts2,r

for i in range(N):
    if i%10==0:
        print i
    teacher = create_teacher(name1,all_names)
    learner = create_learner(name2,all_names)
    cumrew = []
    model_percepts1 = None
    model_percepts2 = None
    action1 = ""
    action2 = ""
    previous = []
    for j in range(n):

        action1 = teacher.update_models(None,(model_percepts1))
        action2 = learner.update_models(None,(model_percepts2))
        #print action1
        #print "------------------"+action2
        model_percepts1,model_percepts2,r = world_update(action1,action2,previous)
        cumrew.append(r)

    CUMREW+=(np.arange(n) - np.cumsum(np.array(cumrew)))/float(N)

plt.plot(CUMREW)
plt.show()