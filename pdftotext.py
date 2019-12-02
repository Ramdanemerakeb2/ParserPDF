import shutil   #pour suprimmer récursivement
import subprocess as sp #commande 
import os       #commande de base
import os.path  #le path du program
import sys      #argument 

def compareStr(str1, str2):
    if len(str1) == len(str2):
        cpt = 0
        while cpt < len(str1):
            if ord(str1[cpt]) == ord(str2[cpt]) or ord(str1[cpt]) == (ord(str2[cpt])+32) or ord(str1[cpt]) == (ord(str2[cpt])-32):
                cpt+=1
            else : return False
        return True
    return False

def findTitle(src, dst, element):
    title = author = ""
    debut = finished = False
    element = element[:-4]
    for char in element :
        if char == '_':
            break
        author+=char
    for ligne in src:
        if not debut :
            save = ""
            cpt = 0
            done = False
            while not done :
                for char in ligne :
                    if char == " " :
                        cpt+=1
                    if cpt < 2 and char != ":" :
                        save +=char
                if title == "" :
                    cpt = 0
                    for char in element :
                        if char == " " :
                            cpt+=1
                        if cpt < 2 and char != ":" :
                            title +=char
                            if char == "_" :
                                title = ""
                done = True
            if compareStr(title, save) : 
                debut = True
                print(ligne, file = dst)
        else if not finished:
            done = False
            for char in ligne :
                while not done :
                    if compareStr(title, save) : 
                        debut = True
                        if (ord(char) >= 65 and ord(char) <= 90) or if (ord(char) >= 97 and ord(char) <= 122) :
                            tmpAuthor += char


        

def filtre(src, dst, element):
    findTitle(src, dst, element)

# Transform an element to a terminal friendly element
def transform(element):
    cpt = 0
    for i in element :
        if i == " " :
            element = element[:cpt] + '\ ' + element[cpt+1:]
            cpt+=1
        cpt+=1
    return element
            
def pdf(arg):
    tmp = "{}/tmp".format(arg)
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.mkdir(tmp)
    for element in os.listdir(arg):
        if element.endswith('.pdf'):
            element = transform(element)
            titre = element[0:-4]
            a = "pdftotext -raw -nopgbrk -enc ASCII7 {0}/{1}/{2}  {0}/{1}/tmp/{3}.txt".format(os.getcwd(),arg, element, titre)
            os.system(a)

def transmog(arg):
    origin = "{0}/{1}".format(os.getcwd(), arg)
    result = "{0}/{1}result".format(os.getcwd(), arg)
    if os.path.exists(result):
        shutil.rmtree(result)
    os.mkdir(result)
    tmp = "{0}/{1}/tmp".format(os.getcwd(), arg)
    for element in os.listdir(tmp):
        if element.endswith('.txt'):
            os.chdir(tmp)
            source = open(element,"r")
            destination = open(result+'/'+element, "w")
            filtre(source,destination, element)
            source.close()
            destination.close()
    os.chdir(origin)
 

def main(argv):               
    if len(argv) != 2:
        print("Un seul argument attendu !")
        print(argv)
        sys.exit(2)
    else:
        current = os.getcwd()
        if os.path.exists(argv[1]) & os.path.isdir(argv[1]):
            pdf(argv[1])
            transmog(argv[1])
            #os.system("rm -r tmp")
        else:
            print( "L'argument n'existe pas ou n'est pas un répertoire !")
            sys.exit(2)


main(sys.argv)