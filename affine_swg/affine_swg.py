import copy



def InitializeMatrixAndBackTrack(s, t):
    matrix = []
    layer = []
    back_track = []
    layer_b = []

    for i in range(len(s)+1):
        layer.append([0 for j in range(len(t)+1)])
        layer_b.append(["" for j in range(len(t)+1)])
    
    layer_lower = copy.deepcopy(layer)
    layer_middle = copy.deepcopy(layer)
    layer_upper = copy.deepcopy(layer)
    
    layer_b_lower = copy.deepcopy(layer_b)
    layer_b_middle = copy.deepcopy(layer_b)
    layer_b_upper = copy.deepcopy(layer_b)


    for i in range(len(t)+1):
        layer_lower[0][i] = float('-inf')
    for i in range(len(s)+1):
        layer_upper[i][0] = float('-inf')

    matrix.append(layer_lower)
    matrix.append(layer_middle)
    matrix.append(layer_upper)

    back_track.append(layer_b_lower)
    back_track.append(layer_b_middle)
    back_track.append(layer_b_upper)

    
    # initialize the lower layer
    for i in range(len(t)+1):
        matrix[0][0][i] = float('-inf')
    # initialize the upper layer
    for i in range(len(s)+1):
        matrix[2][i][0] = float('-inf')

    # print("lower")
    # for j in range(len(matrix[0])):
    #     print(matrix[0][j])

    # print("mid")
    # for j in range(len(matrix[0])):
    #     print(matrix[1][j])
    
    # print("upper")
    # for j in range(len(matrix[0])):
    #     print(matrix[2][j])

    return matrix, back_track

def ConstructMatrixAffine(match_reward, mismatch_penalty, sigma, epsilon, s, t):

    matrix, back_track = InitializeMatrixAndBackTrack(s, t)

    for i in range(len(s)+1):
        for j in range(len(t)+1):
            # skip i-0, j=0
            if i == 0 and j == 0:
                continue
            match = 0
            if s[i-1] == t[j-1]:
                match = match_reward
            else:
                match = -mismatch_penalty

            if i != 0:
                # update lower layer: index 0
                matrix[0][i][j] = max(matrix[0][i-1][j]-epsilon, matrix[1][i-1][j]-sigma)
                # update back_track matrix
                if matrix[0][i][j] == matrix[0][i-1][j]-epsilon:
                    back_track[0][i][j] = "u"
                elif matrix[0][i][j] == matrix[1][i-1][j]-sigma:
                    back_track[0][i][j] = "mid"

            if j != 0:
                # udpate upper layer: index 2
                matrix[2][i][j] = max(matrix[2][i][j-1]-epsilon, matrix[1][i][j-1]-sigma)
                # update back_track matrix
                if matrix[2][i][j] == matrix[2][i][j-1]-epsilon:
                    back_track[2][i][j] = "l"
                elif matrix[2][i][j] == matrix[1][i][j-1]-sigma:
                    back_track[2][i][j] = "mid"

            # update middle layer: index
            if (i != 0 and j != 0):
                matrix[1][i][j] = max(matrix[0][i][j], matrix[1][i-1][j-1]+match, matrix[2][i][j])
                if matrix[1][i][j] == matrix[0][i][j]:
                    back_track[1][i][j] = "lower"
                elif matrix[1][i][j] == matrix[2][i][j]:
                    back_track[1][i][j] = "upper"
                elif matrix[1][i][j] == matrix[1][i-1][j-1]+match_reward and (i != 0 and j !=0):
                    back_track[1][i][j] = "match"
                elif matrix[1][i][j] == matrix[1][i-1][j-1]-mismatch_penalty and (i != 0 and j !=0):
                    back_track[1][i][j] = "mismatch"
            else:
                matrix[1][i][j] = max(matrix[0][i][j], matrix[2][i][j])
                if matrix[1][i][j] == matrix[0][i][j]:
                    back_track[1][i][j] = "lower"
                elif matrix[1][i][j] == matrix[2][i][j]:
                    back_track[1][i][j] = "upper"

    return back_track, matrix[1][len(s)][len(t)]


def BackTrackV(back_track, v, i, j, k):
    # k is the layer num
    # print(i, j, k)
    # print(back_track[k][i][j])
    if back_track[k][i][j] == '':
        # print("Enter ending")
        return ""
    if back_track[k][i][j] == "u":
        return BackTrackV(back_track, v, i-1, j, k) + v[i-1]
    elif back_track[k][i][j] == "l":
        return BackTrackV(back_track, v, i, j-1, k) + "-"
    elif back_track[k][i][j] == "mid":
        if k == 0:
            k = 1
            return BackTrackV(back_track, v, i-1, j, k) + v[i-1]
        elif k == 2:
            k = 1
            return BackTrackV(back_track, v, i, j-1, k) + "-"
    elif back_track[k][i][j] == "lower":
        k = 0
        return BackTrackV(back_track, v, i, j, k)
    elif back_track[k][i][j] == "upper":
        k = 2
        return BackTrackV(back_track, v, i, j, k)
    elif back_track[k][i][j] == "match" or "mismatch":
        return BackTrackV(back_track, v, i-1, j-1, k) + v[i-1]
    

def BackTrackW(back_track, w, i, j, k):
    # k is the layer num

    if back_track[k][i][j] == '':
        # print("Enter ending")
        return ""
    if back_track[k][i][j] == "u":
        return BackTrackW(back_track, w, i-1, j, k) + "-"
    elif back_track[k][i][j] == "l":
        return BackTrackW(back_track, w, i, j-1, k) + w[j-1]
    elif back_track[k][i][j] == "mid":
        if k == 0:
            k = 1
            return BackTrackW(back_track, w, i-1, j, k) + "-"
        elif k == 2:
            k = 1
            return BackTrackW(back_track, w, i, j-1, k) + w[j-1]
    elif back_track[k][i][j] == "lower":
        k = 0
        return BackTrackW(back_track, w, i, j, k)
    elif back_track[k][i][j] == "upper":
        k = 2
        return BackTrackW(back_track, w, i, j, k)
    elif back_track[k][i][j] == "match" or "mismatch":
        return BackTrackW(back_track, w, i-1, j-1, k) + w[j-1]
    
# Insert your AffineAlignment function here, along with any subroutines you need
def AffineAlignment(match_reward: int, mismatch_penalty: int,
                    gap_opening_penalty: int, gap_extension_penalty: int,
                    s: str, t: str) -> Tuple[int, str, str]:
    m = len(s)
    n = len(t)
    back_track, score = ConstructMatrixAffine(match_reward, mismatch_penalty, gap_opening_penalty, gap_extension_penalty, s, t)
    v = BackTrackV(back_track, s, m, n, 1)
    w = BackTrackW(back_track, t, m, n, 1)

    return score, v, w