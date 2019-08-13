
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib2
import os
from os import path
from datetime import datetime, timedelta
import zipfile

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


def unzipfile(script_path,relpath):
    extension=".zip"
    file_name=relpath
    abs_file_path=os.path.join(script_path,file_name)
    zip_ref=zipfile.ZipFile(abs_file_path)
    zip_ref.extract(abs_file_path)
    zip_ref.close()
    os.remove(abs_file_path)

def unzip1(file_name):
    fh=open(file_name+".zip",'rb')
    z=zipfile.ZipFile(fh)
    for name in z.namelist():
        outpath=os.getcwd()+"/domains/"+file_name
        z.extract(name,outpath)
    fh.close()
    os.remove(file_name+".zip")

def file_is_empty(path):
    return os.stat(path).st_size==0

def CheckFolder(folder):
    if os.path.isdir("domains/"+folder):
     return True
    else:
     return False
def CheckFile(file,folder):
    if os.path.exists("domains/"+folder+"/"+file+".txt"):
        print "This checkfile returns true "+ file
        return True
    else:
        print "This checkfile returns false "+ file
        return False

def GetDates(days,now=False):
    n=days
    mylist=[]
    datenow=datetime.now()
    today=datetime.strftime(datenow,"%Y-%m-%d")
    date_N_days_ago=datetime.now() - timedelta(days=n)
    future=datetime.strftime(date_N_days_ago,"%Y-%m-%d")
    mylist.append(today)
    mylist.append(future)

    #print (datetime.now())
    #print (date_N_days_ago)
    #print mylist[0]
    #print mylist[1]
    if now==True:
        return mylist[0]
    else:
        return mylist[1]



def SaveResults(exp,file,folder):
    global input_pathname
    input_pathname = folder+".txt"
    file1="domain-names"
    if CheckFile(input_pathname,folder)==True:
        input_pathname = folder+".txt"
        print input_pathname
    elif CheckFile(file1,folder)==True:
        input_pathname="domain-names.txt"
        print input_pathname

    savepath = os.getcwd() + "/domains/" + folder + "/"
    input_path=savepath+input_pathname



    with open(input_path,"r") as  inputfile,\
        open(savepath+file,'w') as outputfile:
        for line in inputfile:
            if re.match(exp,line):
                outputfile.write(line)
                print (line)

def download(url,file_name):
    url = url

    #file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print ("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print (status),

    f.close()




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

num="2017-07-12"
url1=("https://whoisds.com//whois-database/newly-registered-domains/%s.zip/nrd" %num)

TodayNow=GetDates(0)
FutureNow=GetDates(7)
working_directory="c:\\otherscripts"
script_path=os.path.abspath(__file__)
script_dir=os.path.split(script_path)[0]

#file_path=os.path.split("otherscripts")


print TodayNow
print FutureNow

for i in range(8):
    num=GetDates(i)
    print i
    url=("https://whoisds.com//whois-database/newly-registered-domains/%s.zip/nrd" %num)
    print url
    download(url,num+".zip")
    if CheckFolder(num)==True:
        print "This folder already exists"
        os.remove(num+".zip")
    elif file_is_empty(num+".zip")==True:
        print "The file is empty going to delete"
        os.remove(num+".zip")
    else:
        print "The file is not empty going to keep it"
        unzip1(num)
        SaveMultipleResults(num)

#download(url1,"2017-07-12.zip")






#output_file = "extracted_numbers.txt"
