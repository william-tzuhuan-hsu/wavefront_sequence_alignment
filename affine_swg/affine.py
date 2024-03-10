import sys
from typing import List, Dict, Iterable, Tuple
import numpy

def AffineAlignment_Updated(match_reward: int, mismatch_penalty: int,
                    gap_opening_penalty: int, gap_extension_penalty: int,
                    s: str, t: str) -> Tuple[int, str, str]:
    lower, middle, upper = CreateTraceback(match_reward, mismatch_penalty, gap_opening_penalty, gap_extension_penalty, s, t)
    aligned_v = ""
    aligned_w = ""
    i, j = len(s), len(t)
    current_layer = 1
    while i > 0 or j > 0:
        if current_layer == 0:
            if i > 0 and lower[i][j] == middle[i-1][j] + gap_opening_penalty:
                current_layer = 1
                aligned_v = s[i - 1] + aligned_v
                aligned_w = "-" + aligned_w
            elif i > 0 and lower[i][j] == lower[i-1][j] + gap_extension_penalty:
                current_layer = 0
                aligned_v = s[i - 1] + aligned_v
                aligned_w = "-" + aligned_w
            elif j == 0 and upper[i][j] == middle[i][j-1] + gap_opening_penalty + gap_extension_penalty:
                current_layer = 2
                aligned_v = s[i - 1] + aligned_v
                aligned_w = "-" + aligned_w
            i -= 1

        elif current_layer == 1:
            if i > 0 and middle[i][j] == lower[i][j]:
                current_layer = 0
            elif j > 0 and middle[i][j] == upper[i][j]:
                current_layer = 2
            else:
                aligned_v = s[i - 1] + aligned_v
                aligned_w = t[j - 1] + aligned_w
                i -= 1
                j -= 1
        
        elif current_layer == 2:
            if j > 0 and upper[i][j] == middle[i][j-1] + gap_opening_penalty:

                current_layer = 1
                aligned_v = "-" + aligned_v
                aligned_w = t[j - 1] + aligned_w

            elif j > 0 and upper[i][j] == upper[i][j-1] + gap_extension_penalty:
                current_layer = 2
                aligned_v = "-" + aligned_v
                aligned_w = t[j - 1] + aligned_w
            
            elif i == 0 and upper[i][j] == middle[i][j-1] + gap_opening_penalty + gap_extension_penalty:
                current_layer = 2
                aligned_v = "-" + aligned_v
                aligned_w = t[j - 1] + aligned_w
            j -= 1
    

    return middle[len(s)][len(t)], aligned_v, aligned_w



def CreateTraceback(match, mismatch, gap_opening, gap_extension, s, t):
    lower = [[float('inf')] * (len(t) + 1) for _ in range(len(s) + 1)]
    middle = [[float('inf')] * (len(t) + 1) for _ in range(len(s) + 1)]
    upper = [[float('inf')] * (len(t) + 1) for _ in range(len(s) + 1)]

    # Initialize the matrices
    lower[0][0] = float('inf')
    middle[0][0] = 0
    upper[0][0] = float('inf')

    for i in range(1, len(s) + 1):
        lower[i][0] = gap_opening + (i) * gap_extension
        middle[i][0] = gap_opening + (i) * gap_extension
        upper[i][0] = float('inf')

    for j in range(1, len(t) + 1):
        upper[0][j] = gap_opening + (j) * gap_extension
        middle[0][j] = gap_opening + (j) * gap_extension
        lower[0][j] = float('inf')

    # Fill in the matrices
    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            lower[i][j] = min(lower[i - 1][j] + gap_extension, middle[i - 1][j] + gap_opening)
            upper[i][j] = min(upper[i][j - 1] + gap_extension, middle[i][j - 1] + gap_opening)
            if s[i - 1] == t[j - 1]:
                diagonal = middle[i - 1][j - 1] + match
            else:
                diagonal = middle[i - 1][j - 1] + (mismatch)
            middle[i][j] = min(lower[i][j], upper[i][j], diagonal)
    return lower, middle, upper

match_reward = 1
mismatch_penalty = 3
gap_opening_penalty = 2
gap_extension_penalty = 1
s = "GA"
t = "GTTA"
## (-1, 'G--A', 'GTTA')

# match_reward = 5
# mismatch_penalty = 2
# gap_opening_penalty = 15
# gap_extension_penalty = 5
# s = "ACGTA"
# t = "ACT"
## (-12, 'ACGTA', 'ACT--')


# match_reward = 1
# mismatch_penalty = 5
# gap_opening_penalty = 5
# gap_extension_penalty = 1
# s = "GAT"
# t = "AT"

# match_reward = 1
# mismatch_penalty = 5
# gap_opening_penalty = 2
# gap_extension_penalty = 1
# s = "CCAT"
# t = "GAT"
## (-3, '-CCAT', 'G--AT')

AffineAlignment_Updated(match_reward, mismatch_penalty, gap_opening_penalty, gap_extension_penalty, s, t)
# score, align_s, align_t = AffineAlignment(match_reward, mismatch_penalty, gap_opening_penalty, gap_extension_penalty, s, t)
# print("Alignment Score:", score)
# print("Alignment s:", align_s)
# print("Alignment t:", align_t)