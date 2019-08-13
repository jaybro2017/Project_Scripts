import re

#Declare variables

numbers = r'^\b\d\S*\.([a-zA-Z0-9])\S*'
A = r'^\b[a[A]\S*\.([a-zA-Z0-9])\S*'
B = r'^\b[b[B]\S*\.([a-zA-Z0-9])\S*'
C = r'^\b[c[C]\S*\.([a-zA-Z0-9])\S*'
D = r'^\b[d[D]\S*\.([a-zA-Z0-9])\S*'
E = r'^\b[e[E]\S*\.([a-zA-Z0-9])\S*'
F = r'^\b[f[F]\S*\.([a-zA-Z0-9])\S*'
G = r'^\b[g[G]\S*\.([a-zA-Z0-9])\S*'
H = r'^\b[h[H]\S*\.([a-zA-Z0-9])\S*'
I = r'^\b[i[I]\S*\.([a-zA-Z0-9])\S*'
J = r'^\b[j[J]\S*\.([a-zA-Z0-9])\S*'
K = r'^\b[k[K]\S*\.([a-zA-Z0-9])\S*'
L = r'^\b[l[L]\S*\.([a-zA-Z0-9])\S*'
M = r'^\b[m[M]\S*\.([a-zA-Z0-9])\S*'
N = r'^\b[n[N]\S*\.([a-zA-Z0-9])\S*'
O = r'^\b[o[O]\S*\.([a-zA-Z0-9])\S*'
P = r'^\b[p[P]\S*\.([a-zA-Z0-9])\S*'
Q = r'^\b[q[Q]\S*\.([a-zA-Z0-9])\S*'
R = r'^\b[r[R]\S*\.([a-zA-Z0-9])\S*'
S = r'^\b[s[S]\S*\.([a-zA-Z0-9])\S*'
T = r'^\b[t[T]\S*\.([a-zA-Z0-9])\S*'
U = r'^\b[u[U]\S*\.([a-zA-Z0-9])\S*'
V = r'^\b[v[V]\S*\.([a-zA-Z0-9])\S*'
W = r'^\b[w[W]\S*\.([a-zA-Z0-9])\S*'
X = r'^\b[x[X]\S*\.([a-zA-Z0-9])\S*'
Y = r'^\b[y[Y]\S*\.([a-zA-Z0-9])\S*'
Z = r'^\b[z[Z]\S*\.([a-zA-Z0-9])\S*'

def SaveResults(exp,file,folder):
    input_pathname = folder+".txt"
    #savepath = os.getcwd() + "/domains/" + folder + "/"
    input_path=input_pathname

    with open(input_path,"r") as  inputfile,\
        open(file,'w') as outputfile:
        for line in inputfile:
            if re.match(exp,line):
                outputfile.write(line)
                print (line)


def SaveMultipleResults(folder):

    SaveResults(numbers,"Domains0-9.txt",folder)
    SaveResults(A,"DomainsA.txt",folder)
    SaveResults(B,"DomainsB.txt",folder)
    SaveResults(C,"DomainsC.txt",folder)
    SaveResults(D,"DomainsD.txt",folder)
    SaveResults(E,"DomainsE.txt",folder)
    SaveResults(F,"DomainsF.txt",folder)
    SaveResults(G,"DomainsG.txt",folder)
    SaveResults(H,"DomainsH.txt",folder)
    SaveResults(I,"DomainsI.txt",folder)
    SaveResults(J,"DomainsJ.txt",folder)
    SaveResults(K,"DomainsK.txt",folder)
    SaveResults(L,"DomainsL.txt",folder)
    SaveResults(M,"DomainsM.txt",folder)
    SaveResults(N,"DomainsN.txt",folder)
    SaveResults(O,"DomainsO.txt",folder)
    SaveResults(P,"DomainsP.txt",folder)
    SaveResults(Q,"DomainsQ.txt",folder)
    SaveResults(R,"DomainsR.txt",folder)
    SaveResults(S,"DomainsS.txt",folder)
    SaveResults(T,"DomainsT.txt",folder)
    SaveResults(U,"DomainsU.txt",folder)
    SaveResults(V,"DomainsV.txt",folder)
    SaveResults(W,"DomainsW.txt",folder)
    SaveResults(X,"DomainsX.txt",folder)
    SaveResults(Y,"DomainsY.txt",folder)
    SaveResults(Z,"DomainsZ.txt",folder)

Search = input('Input file name for domain extraction eg. domains.txt ')

SaveMultipleResults(Search)

