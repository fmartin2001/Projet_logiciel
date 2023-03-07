
# Mutation function
def mutation(P, Tm):
    n, m, o,q = P.shape
    P_copy = np.copy(P)
    for i in range(n):
        for j in range(m):
            for k in range(o):
                for l in range(q):
                    p = np.random.random()
                    if p < Tm:
                        P_copy[i, j,k,l] = (0.5) * P[i, j,k,l]
    return P_copy


def crossing_over_temp(P, Tc):
    new_P = np.copy(P)
    liste = []

    for i in range(0, len(new_P)):
        if random() < Tc:
            indc_im = randint(0, new_P.shape[0] - 1)
            posc_x = randint(0, new_P.shape[1] - 1)
            posc_y = randint(0, new_P.shape[2] - 1)
            posc_z = randint(0, new_P.shape[3] - 1)
            tmp = new_P[i, posc_x:new_P.shape[1], posc_y:new_P.shape[2], posc_z:new_P.shape[3]]
            new_P[i, posc_x:new_P.shape[1], posc_y:new_P.shape[2], posc_z:new_P.shape[3]] = new_P[indc_im,
                                                                                            posc_x:new_P.shape[1],
                                                                                            posc_y:new_P.shape[2],
                                                                                            posc_z:new_P.shape[3]]
            new_P[indc_im, posc_x:new_P.shape[1], posc_y:new_P.shape[2], posc_z:new_P.shape[3]] = tmp
            liste.append(indc_im)

    return new_P, liste