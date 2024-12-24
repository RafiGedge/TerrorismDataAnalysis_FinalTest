import numpy as np


def get_correlation(data):
    return float(np.corrcoef(range(len(data)), data)[0, 1])
