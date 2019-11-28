import shutil   #pour suprimmer récursivement
import subprocess as sp #commande 
import os       #commande de base
import os.path  #le path du program
import sys      #argument 

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
    origin = "{0}/{1}".format(os.getcwd(), arg)
    result = "{0}/{1}result".format(os.getcwd(), arg)
    if os.path.exists(result):
        shutil.rmtree(result)
    os.mkdir(result)
    tmp = "{0}/{1}/tmp".format(os.getcwd(), arg)
    for element in os.listdir(tmp):
        if element.endswith('.txt'):
            #element = transformEintoE(element)
            os.chdir(tmp)
            source = open(element,"r")
            destination = open(result+'/'+element, "w")
            filtre(source,destination)
            source.close()
            destination.close()
    print(origin)
    os.chdir(origin)
            
            
            
            
if len(sys.argv) != 2:
    print("Un seul argument attendu !")
    print(sys.argv)
    sys.exit(2)
else:
    current = os.getcwd()
    if os.path.exists(sys.argv[1]) & os.path.isdir(sys.argv[1]):
        pdf(sys.argv[1])
        transmog(sys.argv[1])
        os.system("rm -r tmp")
    else:
        #print(sys.argv[1])
        print( "L'argument n'éxiste pas ou n'est pas un répertoire !")
        sys.exit(2)
