import numpy as np

import math

def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def length(v):
    return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
    return math.degrees(math.acos(dotproduct(v1, v2) / (length(v1) * length(v2))))


def convert_to_variables(data):
    Ds = np.zeros((len(data) - 1, data.shape[1]))
    Vs = np.zeros((data.shape[0] - 1))

    for i in range(len(data) - 1):
        Ds[i] = data[i+1] - data[i]
    z = [0,0,1]
    for i in range(len(data) -1):
        Vs[i] = angle(Ds[i], z)

    s = np.zeros(Ds.shape[0] - 1)
    sV = np.zeros(Ds.shape[0] - 1)
    for i in range(0, Ds.shape[0] - 1):
        s[i] = np.sign(np.dot(Ds[i+1], Ds[i]))
        sV[i] = s[i] * Vs[i]
    return sV
