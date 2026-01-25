from config import t

from typing import List, Union
import numpy as np


def differentiate(f: List[float]) -> List[float]:
    """
    Computes the discrete derivative of a list of values over time t.
    """
    return [(f[i+1] - f[i]) / t for i in range(len(f) - 1)]


def integrate(f: List[float]) -> List[float]:
    """
    Computes the discrete integral of a list of values over time t using the Euler method.
    """
    F = [0.0]
    for i in range(len(f)):
        F.append(F[-1] + t * f[i])
    return F


def least_squares_method(x: np.ndarray, y: np.ndarray) -> float:
    """
    Computes the slope of the linear regression line for data points (x, y) using the least squares method.
    """
    s = sum(x)
    n = len(x)
    return (n * np.dot(x, y) - s * sum(y)) / (n * np.dot(x, x) - s ** 2)