import shutil   #pour suprimmer recursivement
import subprocess as sp #commande 
import os       #commande de base
import os.path  #le path du program
import sys      #argument 
from bs4 import BeautifulSoup

def transformEintoE(element):
    cpt = 0
    for i in element :
        if i == " " :
            element = element[:cpt] + '\ ' + element[cpt+1:]
            cpt+=1
        cpt+=1
    print(element)
    return element

def filtre(src,dst):
    for ligne in src:
        print(ligne, file=dst)
        
        
def pdf(arg):
    tmp = "{}/tmp".format(arg)
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.mkdir(tmp)
    for element in os.listdir(arg):
        if element.endswith('.pdf'):
            print(os.getcwd())
            element = transformEintoE(element)
            titre = element[0:-4]
            a = "pdftotext -raw -nopgbrk -enc ASCII7 {0}/{1}/{2}  {0}/{1}/tmp/{3}.txt".format(os.getcwd(),arg, element, titre)
            #print(a)
            os.system(a)
          #  sp.run(["pdf2txt","-o" ,arg,"/tmp/",element, ".txt ", arg,element])
        #  a = "pdf2txt -p[1] {1}/{2} > {1}/tmp/{2}.txt".format(os.getcwd(),arg, element) 
        
        

def transmog(arg):
    result = "{0}/{1}result".format(os.getcwd(), arg)
    if os.path.exists(result):
        shutil.rmtree(result)
    os.mkdir(result)
    tmp = "{0}/{1}/tmp".format(os.getcwd(), arg)
    for element in os.listdir(tmp):
        if element.endswith('.txt'):
            a = "../result/"
            #element = transformEintoE(element)
            os.chdir(tmp)
            source = open(element,"r")
            destination = open(a+element, "w")
            #filtre(source,destination)
            source.close()
            destination.close()


def transmogXML(arg):
    result = "{0}/{1}result".format(os.getcwd(), arg)
    if os.path.exists(result):
        shutil.rmtree(result)
    os.mkdir(result)
    tmp = "{0}/{1}/tmp".format(os.getcwd(), arg)
    for element in os.listdir(tmp):
        if element.endswith('.xml'):
            a = "../result/"
            os.chdir(tmp)
            source = open(element,"r")
            destination = open(a+element, "w")
            source.close()
            destination.close()   
            
            
            
            
if len(sys.argv) > 3:
    print("Deux arguments attendu au maximum !")
    print(sys.argv)
    sys.exit(2)
if len(sys.argv) == 1:
    current = os.getcwd()
    if os.path.exists(sys.argv[1]) & os.path.isdir(sys.argv[1]):
        pdf(sys.argv[2])
        transmog(sys.argv[2])
        sys.exit(2)
    else:
        print( "L'argument n'existe pas ou n'est pas un repertoire !")
        sys.exit(2)
if len(sys.argv) == 2 :
    if sys.argv[1] == "-t":
        if os.path.exists(sys.argv[1]) & os.path.isdir(sys.argv[1]):
            pdf(sys.argv[2])
            transmog(sys.argv[2])
        else:
            print( "L'argument n'existe pas ou n'est pas un repertoire !")
            sys.exit(2)
    elif sys.argv[1] == "-x":
        if os.path.exists(sys.argv[1]) & os.path.isdir(sys.argv[1]):
            pdf(sys.argv[2])
            transmogXML(sys.argv[2])
            sys.exit(2)
        else:
            print( "L'argument n'existe pas ou n'est pas un repertoire !")
            sys.exit(2)
    else:
         print( "Veuillez choisir un type de sortie convenable (-x ou -t)")     
         sys.exit(2)   

#librairie beautifultree pour XML