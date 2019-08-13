from Wappalyzer import Wappalyzer, WebPage
from bs4 import BeautifulSoup
import sys
import csv
import whois
import os
import lxml
import argparse



parser = argparse.ArgumentParser(description='Automatic function please use --auto or -a with the other arguements')

parser.add_argument('-a','--auto', help='Enable auto command to run script',required=False)
parser.add_argument('-s','--search', help='Search file *.txt',required=False)
parser.add_argument('-d','--domains', help='Domains file *.txt',required=False)
parser.add_argument('-r','--results', help='Results file *.csv',required=False)
args=parser.parse_args()

if args.auto:
    Search=args.search
    DomainsA=args.domains
    ResultsA=args.results
else:
    Search = input('Input file name for search query eg. search.txt ')
    DomainsA = input('Input file name for domains eg. domains.txt ')
    ResultsA = input('Input file name for results eg. results.csv ')

def GetSearchQuery(f,title):
    l=[]
    with open(f, 'r') as file:
        for line in file:
            content=line.rstrip('\n')
            if title=="Title":
                l.append(content)
            else:
                l.append(u'{0}'.format(content))
            #print l
    return l

main=['Website','Status','Contact']
Fields=GetSearchQuery(Search,"Title")
#fieldnames = ['Website', 'Status','Contact', 'Wordpress', 'WooCommerce','PHP','Shopify']
main.extend(Fields)

def csv_writerheader(path):
    with open(path,'a',newline='',encoding='utf8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=main, lineterminator='\n')
        writer.writeheader()

def CheckFile(f):
    if os.path.isfile(f):
     return True
    else:
     return False

def GetWhois(web):
    try:
         xwhois=whois.whois(web)
         print (xwhois.emails)
         if 'No match for' in xwhois:
             error="Nothing"
             return error
         elif not xwhois.emails==None:
          email=xwhois.emails
          return email
         
         else:
             error="Nothing"
             return error
    except:
        error="Nothing"
        return error
 
def print_text(d):
        #print("sleeping for (%d)sec" % d)
        print(d)

def isok(mypath):
    try:
        print ("isok step1")
        print (mypath)
        http=urllib3.PoolManager()
        #urllib3.disable_warnings()
        response = http.request('Get',mypath)#,timeout = 5)
        soup=BeautifulSoup(response.data, "lxml")
        print (soup.status)
    except urllib3.exceptions.HTTPError as e:
        print ("HTTP ERROR")
        return 0
    except urllib3.exceptions.NewConnectionError as e:
        print ("URL ERROR")
        return 0
    #except http.client.HTTPException as e:
     #   print ("HTTP Exception ERROR")
      #  return 0
    #except socket.error as e:
     #   print ("Socket Error")
      #  return 0
    else:
        return 1

def toUnicode(s):
    if type(s) is unicode:
        return s
    elif type(s) is str:
        d = chardet.detect(s)
        (cs, conf) = (d['encoding'], d['confidence'])
        if conf > 0.80:
            try:
                return s.decode( cs, errors = 'replace' )
            except Exception as ex:
                pass 
   
    return unicode(''.join( [ i if ord(i) < 128 else ' ' for i in s ]))

def RemoveText(fil,li):
 f = open(fil,'r')
 words = [li]
 lst = []
 for line in f:
    if not any(word in line for word in words):
     lst.append(line)
 f.close()
 f = open(fil,'w')
 for line in lst:
    f.write(line)
 f.close()




def PrintWeb(f,res):
    # Open the file for reading.
  global x
  print ("Step 2")
  with open(f, 'r') as infile:

      data = infile.read()  # Read the contents of the file into memory.

      # Return a list of the lines, breaking at line boundaries.
      my_list = data.splitlines()
      for line in my_list:
        #alist=[u'WordPress',u'WooCommerce',u'PHP',u'Shopify']
        alist=GetSearchQuery(Search,"s")
        http="http://www."+line.title()
        htp="http://httpbin.org/status/404"
        hp="http://www.Abogadosva.Com"
        agent="user_agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        html=''
        #web=isok(http)
        web=True
        if web:
            print ("website exists")
            print ("The website we are working on " +http)
            
            
            try:
                wappalyzer = Wappalyzer.latest()
                webpage = WebPage.new_from_url(http,agent)
                x=wappalyzer.analyze(webpage)
            except ValueError as e:
                print ("This is error value")
                print (e)
                pass
                print ("Removing Text "+line.title())
                RemoveText(f,line)#removes domain from text file
            
                
            
            if x:
                  print (x)
                  print ("Removing Text "+line.title())
                  RemoveText(f,line)#removes domain from text file
                  blist=list(x)
                  contact=GetWhois(line.title())
                  l=[]
                  li=[http,'avaliable',contact]
                  z=get_list(alist,blist,l)
                  li.extend(z)
                  print (li)   
                  WriteCsv(li,res)
                  
            else:
                 print("Error with http request")
                 RemoveText(f,line)
        else:
            print("Website does not exist " +http)
            RemoveText(f,line) 
 


def wait_delay(d):
        print("sleeping for (%d)sec" % d)
        sleep(d)

def get_list(alist,blist,li):
 
 for x in alist:
     if x in alist:
         z=alist.index(x)
     else:
          print (None)

     if x in blist:
        a="Yes"
        li.insert(z,a) 
     else:
        b="No"
        li.insert(z,b)

 return li    

def WriteCsv(list,results):
    exist=CheckFile(results)
    
    
    try:
        if exist:
         #print (list)
         print ("File Exists")
        else:
         print ("File does not exist")
         csv_writerheader(results)
        with open(results, 'a',newline='',encoding='utf8') as csvfile:
              writer = csv.writer(csvfile, delimiter=',')
              try:
                 writer.writerow(list)
              except IOError as er:
                    print ("Could not write file:")
                    print (er)
    except IOError as ere:
           print ("Could not open file:")
           print (ere)



#delays = [randrange(3, 7) for i in range(50)]

#print ThreadPool.ageofqueen

#ResultsB="ResultsB.csv"
#DomainsB="DomainsB.txt"
#DomainsA=input('Input file name for domains eg. filename.txt')
#ResultsA=input('Input file name for results eg. results.csv')
try:
    print("step 1")
    PrintWeb(DomainsA,ResultsA)
except:
    print ("Could not start function")
    #sys.exit()
    pass
    print ("Could not parse Domain, Skipping to next one... ")
    PrintWeb(DomainsA,ResultsA)
else:
    print ("Finished with all the domains not able to run, now exiting....")
    sys.exit()

#pool = ThreadPool.ThreadPool(5) # 20 threads
#pool.add_task(PrintWeb,DomainsA)
#pool.add_task(PrintWeb,DomainsB)
#pool.map(wait_delay, delays)
#pool.wait_completion()

