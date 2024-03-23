def wf_align(q, t, P):
    n = len(q)
    m = len(t)
    # diagonal and offset
    a_k = (m-n)
    a_offset = m
    # initial condition
    M = {}
    I = {}
    D = {}
    s = 0
    M[s] = [0]

    while True:
        # exact extend wavefront
        wf_extend(M[s], q, t)
        # check exit condition
        ########## need to think about indexing ###########
        # if M[s][a_k] >= a_offset:
        #     break
        s += 1
        wf_next(M, I, D, q, t, s, P)
        # break
    return M

def wf_extend(Ms, q, t):
    for k in range(len(Ms)):
        v = Ms[k] - k
        h = Ms[k]
        while q[v] == t[h]:
            Ms[k] = Ms[k]+1
            v += 1
            h += 1
    print(Ms)

def wf_next(M, I, D, q, t, s, P):
    x = P[0]
    o = P[1]
    e = P[2]
    M_hi_x = FindHigh(M, s-x)
    M_hi_o_e = FindHigh(M, s-o-e)
    I_hi_e = FindHigh(I, s-e)
    D_hi_e = FindHigh(D, s-e)
    hi = max(M_hi_x, M_hi_o_e, I_hi_e, D_hi_e)+1

    M_low_x = FindLow(M, s-x)
    M_low_o_e = FindLow(M, s-o-e)
    I_low_e = FindLow(I, s-e)
    D_low_e = FindLow(D, s-e)

    low = max(M_low_x, M_low_o_e, I_low_e, D_low_e)-1
    
    for k in range(low, hi):



def FindHigh(M, score):

if __name__ == "__main__":
    wf_align("GATACA", "GAGATA", [4, 6, 2])