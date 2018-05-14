from plot import *
def getNDF(L):
    L1 = sorted(L, key=lambda x:x[0][1], reverse=True)
    L2 = sorted(L, key=lambda x:x[0][0])
    checked = []
    NDF = []
    newNDF = []

    cursor = 0

    for i in range(len(L1)):
        #checked.append(L1[i])
        del L2[L2.index(L1[i])]
        R = L1[i]
        cursor += 1

        if len(newNDF) > 0:

            L2.extend(newNDF)
            L2 = sorted(L2, key=lambda x:x[0][0])
            #print(L2)

        for j in range(len(L2)):
            coverMode = coverTest(R, L2[j])
            if coverMode == 0:
                R = None ## added
                break
            else:
                if coverMode == 1:
                    break
                else:
                    Sndf, R = intercept(R, L2[j])
                    if Sndf is not None and len(Sndf)>0 and Sndf[0] is not None:
                        NDF.extend(Sndf)
                        newNDF.extend(Sndf)
                    if R is None: # added
                        break
        if R is not None and len(R) > 0:
            NDF.append(R)
            newNDF.append(R)
    myPlot(L, NDF)
    return NDF

def intercept(Si, Sj):
    NDF = []
    R = Si

    if not checkIntercept(Si, Sj):
        Px = verticalSplit(Si, Sj[0])
        Py = horizontalSplit(Si, Sj[-1])
        NDF, R = split(Si, Px, Py)
        #print('NOT', [NDF], R)
        NDF = [NDF]

    else:
        intersectList = sliceIntercept(Si, Sj) 
        print(intersectList, len(intersectList))
        if len(intersectList) == 0: ## New
            Px = verticalSplit(Si, Sj[0])
            Py = horizontalSplit(Si, Sj[-1]) 
            NDF, R = split(Si, Px, Py)
            #print('len0', NDF, R)
        else:
            for k in range(len(intersectList)):
                Sndf = []
                if R is None:
                    return (NDF, R)
                else:
                    
                    mode, intercept, p = intersectList[k]
                    if mode == 0:
                        Px = verticalSplit(R, p)
                        Sndf, R = split(R, Px, intercept)

                    else:
                        Py = horizontalSplit(R, p)
                        Sndf, R = split(R, intercept, Py)
                if Sndf is not None:
                    NDF.extend([Sndf])


    return (NDF,R)

def coverTest(Si, Sj):
    if Si[0][0] > Sj[0][0] and Si[-1][1] > Sj[0][1]:
        return 0
    elif Si[-1][0] < Sj[0][0] and Si[-1][1] > Sj[0][1]:
        return 1
    else:
        return 2

def verticalSplit(S, P):
    if P[0] <= S[0][0]:
        return (None,0)
    elif P[0] >= S[-1][0]:
        return (None,1)
    for i in range(1, len(S)):
        if P[0] > S[i-1][0] and P[0] <=S[i][0]:
            return getSplit(0, P, S[i-1], S[i])

def horizontalSplit(S, P):
    if P[1] <= S[-1][1]:
        return (None,0)
    elif P[1] >= S[0][1]:
        return (None,1)
    for i in range(1, len(S)):
        if P[1] < S[i-1][1] and P[1] >= S[i][1]:
            return getSplit(1, P, S[i-1], S[i])

def split(S, Px, Py): ## problem may occur
    Sndf = None
    Sr = S

    if Px[0] is None:
        if Px[1] != 1:
            Sndf = None
        else:
            if Py[0] is None and Py[1] != 0:
                Sndf = None
            elif Py[0] is None and Py[1] == 0:
                Sndf = S

    if Py[0] is None:
        if Py[1] == 1:
            Sr = S
        elif Py[1] == 2:
            Sr = S
        else:
            Sr = None

    if Px[0] is not None:
        for i in range(1, len(S)):
            if Px[0] > S[i-1][0] and Px[0] <= S[i][0]:
                Sndf = S[0:i]
                Sndf.append(Px)

    if Py[0] is not None:
        for i in range(1, len(S)):
            if Py[1] < S[i-1][1] and Py[1] >= S[i][1]:
                Sr = [Py]
                Sr.extend(S[i:])
    return (Sndf, Sr)


def sliceIntercept(Si, Sj): # problem might occur
    intersectList = []
    for i in range(1, len(Si)):
        for j in range(1, len(Sj)):
            pi0 = Si[i-1]
            pi1 = Si[i]
            pj0 = Sj[j-1]
            pj1 = Sj[j]

            mi = (pi1[1]-pi0[1])/ float(pi1[0]-pi0[0])
            mj = (pj1[1]-pj0[1])/ float(pj1[0]-pj0[0])
            bi = pi0[1]-mi*pi0[0]
            bj = pj0[1]-mj*pj0[0]

            if abs(mi-mj) > 0.01:
                px = (bj-bi)/float(mi-mj)

                py = mi*px + bi
                if px <= max(pi0[0], pi1[0]) and px >= min(pi0[0], pi1[0]) and px <= max(pj0[0], pj1[0]) and px >= min(pj0[0], pj1[0]):
                    if mi <= mj:
                        intersectList.append((0, (px,py), Sj[j-1]))
                    else:
                        intersectList.append((1, (px,py), Sj[j]))
    return intersectList


def getSplit(mode, P, S1, S2):
    lam = (P[mode] - S2[mode]) / float(S1[mode] - S2[mode])
    if mode == 0: # vertical
        P1 = lam * S1[1] + (1-lam) * S2[1]
        if P1 < P[1]:
            return (None, 2)
        else:
            return (P[0], P1)
    elif mode == 1: # horizontal
        P0 = lam * S1[0] + (1-lam) * S2[0]
        if P0 < P[0]:
            return (None, 2)
        else:
            return (P0, P[1])

def checkIntercept(Si, Sj):
    pi_min = Si[0]
    pi_max = Si[-1]
    pj_min = Sj[0]
    pj_max = Sj[-1]

    if pj_max[1] > pi_min[1]:
        return False
    if pj_min[1] < pi_max[1]:
        return False
    if pj_max[0]< pi_min[0]:
        return False
    if pj_min[0] > pi_max[0]:
        return False
    return True

if __name__ == '__main__':
    L = [[(1,10),(10,1)],[(2.5,9),(3,7),(4.5,6)]]

    getNDF(L)









