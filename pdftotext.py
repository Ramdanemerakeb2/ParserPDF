import shutil   
import subprocess as sp 
import os       
import os.path  
import sys      

<<<<<<< HEAD
def Resumé(Contenu):
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
        resumé = ''.join(b)
        return resumé
        
     
def transformEintoE(element):
=======
def compareStr(str1, str2):
    if len(str1) == len(str2):
        cpt = 0
        while cpt < len(str1):
            if ord(str1[cpt]) == ord(str2[cpt]) or ord(str1[cpt]) == (ord(str2[cpt])+32) or ord(str1[cpt]) == (ord(str2[cpt])-32):
                cpt+=1
            else : return False
        return True
    return False

def findTitle(src, element):
    titleToPrint = title = author = tmpAuthor = ""
    debut = finished = False
    element = element[:-4]
    for char in element :
        if char == '_' or char == '-':
            break
        author+=char
    for ligne in src:
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
    return titleToPrint


        

def filtre(src, dst, element):
    print("Titre : " + findTitle(src, element), file = dst)

# Transform an element to a terminal friendly element
def transform(element):
>>>>>>> 9a616041eb1e139f7e12bcaec4a1cbe917d9f62f
    cpt = 0
    for i in element :
        if i == " " :
            element = element[:cpt] + '\ ' + element[cpt+1:]
            cpt+=1
        cpt+=1
    return element
<<<<<<< HEAD

def resultat(source,destination,element):
	nom = element[:-4] + '.pdf'
	destination.write("nom du fichier : ")
	print(nom, file =destination)
	txt = source.read()
	r = Resumé(txt)
	destination.write("\nResumé : ")
	for i in range(0,len(r)) :                                 
		destination.write(r[i])
    
    #for ligne in src:
        #print(ligne, file=dst)
        
        
def pdftotext(arg):
    tmp = "{}/txtTemporaire".format(arg)
=======
            
def pdf(arg):
    tmp = "{}/tmp".format(arg)
>>>>>>> 9a616041eb1e139f7e12bcaec4a1cbe917d9f62f
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.mkdir(tmp)
    for element in os.listdir(arg):
        if element.endswith('.pdf'):
            element = transform(element)
            titre = element[0:-4]
            a = "pdftotext -raw -nopgbrk -enc ASCII7 {0}/{1}/{2}  {0}/{1}/txtTemporaire/{3}.txt".format(os.getcwd(),arg, element, titre)
            os.system(a)

def transmog(arg):
    origin = "{0}/{1}".format(os.getcwd(), arg)
    result = "{0}/{1}resultat".format(os.getcwd(), arg)
    if os.path.exists(result):
        shutil.rmtree(result)
    os.mkdir(result)
    tmp = "{0}/{1}/txtTemporaire".format(os.getcwd(), arg)
    for element in os.listdir(tmp):
        if element.endswith('.txt'):
            os.chdir(tmp)
            source = open(element,"r")
            destination = open(result+'/'+element, "w")
<<<<<<< HEAD
            resultat(source,destination,element)
=======
            filtre(source,destination, element)
>>>>>>> 9a616041eb1e139f7e12bcaec4a1cbe917d9f62f
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
            pdftotext(argv[1])
            transmog(argv[1])
            #os.system("rm -r tmp")
        else:
            print( "L'argument n'existe pas ou n'est pas un répertoire !")
            sys.exit(2)


main(sys.argv)
