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

def Abstract(Contenu):
    if "Abstract" in Contenu :
        begin = Contenu.split("Abstract",1)
    
    if "ABSTRACT" in Contenu :                                       
        begin = Contenu.split("ABSTRACT",1)                     
                       
    end="1 "
    
    if "Index" in Contenu :
        end = "Index"
    elif "Keywords" in Contenu :                                      
        end = "Keywords"
            
    
    try:
        begin
    except NameError:
        return "erreur"
    else:
        a = begin[1].split(end)
        b = a[0].split("\n")
        abstract = ''.join(b)
        return abstract
        

def findTitle(source, element):
    titleToPrint = title = author = tmpAuthor = ""
    debut = finished = False
    element = element[:-4]
    for char in element :
        if char == '_' or char == '-':
            break
        author+=char
    for ligne in source:
        if ligne == "matically determine the quality of a summary by\n":
            break
        if not debut :
            save = ""
            cpt = 0
            done = False
            while not done :
                for char in ligne :
                    if char == " " :
                        cpt+=1
                    if char == ":":
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
                titleToPrint = ligne
        elif (not finished):
            done = False
            for char in ligne :
                if (ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) :
                    tmpAuthor += char
                else :
                    if compareStr(author, tmpAuthor) : 
                        finished = True
                    else :
                        tmpAuthor = ""
            if not finished :
                titleToPrint = titleToPrint[:-1]
                titleToPrint = titleToPrint + " " +ligne
    return titleToPrint[:-1]


        

def resultat(tmp, result, element):
    os.chdir(tmp)

    source = open(element,"r")
    destination = open(result+'/'+element, "w")
    print("Titre : " + findTitle(source, element), file = destination)
    source.close()

    nom = element[:-4] + '.pdf'
    print("\nnom du fichier : " + nom, file =destination)

    source = open(element,"r")
    txt = source.read()
    r = Abstract(txt)
    destination.write("\nResumé : ")
    for i in range(0,len(r)) :                                 
        destination.write(r[i])
    source.close()
    destination.close()

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
            resultat(tmp, result, element)
    os.chdir(origin)

def xml(arg):  
    for element in os.listdir(arg):
        if element.endswith('.pdf'):
            if not os.path.exists(arg+"/xmlResultat"):
                os.mkdir(arg+"/xmlResultat")
            element = element.replace(".pdf", "")
            source = open(arg+"/result/"+element+".txt", "r")              
            f = open(arg+"/xmlResultat/"+element+".xml", "w")
            i=1
            for line in source:
                if i == 1:
                    t = line
                    t = t[8:-1]
                if i == 3:
                    p = line
                    p = p[17:-1]
                if i == 5:
                    a = line
                    a = a[9:-1]
                i+=1
            f.write("<article>\n")          
            f.write("\t<preamble>"+p+"</preamble>\n")
            f.write("\t<titre>"+t+"</titre>\n")
            f.write("\t<abstract>"+a+"</abstract>\n")
            f.write("</article>")  
            source.close()
 

def main(argv):               
    if len(argv) != 3:
        print("Deux arguments attendus !")
        print("-option attendu :")
        print(" -t  version .txt")
        print(" -x  version .xml")
        sys.exit(2)
    else:
        current = os.getcwd()
        if not (argv[2].endswith("/")) : directory = argv[2] +"/"
        else : directory = argv[2]

        if argv[1] == "-t":
            if os.path.exists(directory) & os.path.isdir(directory):
                pdf(directory)
                transmog(directory)
                os.system("rm -r tmp")
            else:
                print( "L'argument n'éxiste pas ou n'est pas un répertoire !")
                sys.exit(2)
        elif argv[1] == "-x":
            if os.path.exists(directory) & os.path.isdir(directory):
                pdf(directory)
                transmog(directory)
                os.system("rm -r tmp")
                os.chdir(current)
                xml(argv[2])
                os.chdir(current+"/"+directory)
                os.system("rm -r result")
        else :
            print("-option non reconnue :")
            print(" -t  version .txt")
            print(" -x  version .xml")
                    

main(sys.argv)