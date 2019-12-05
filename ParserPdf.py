import shutil   #pour suprimmer récursivement
import subprocess as sp #commande 
import os       #commande de base
import os.path  #le path du program
import sys      #argument 

# compare 2 strings without taking care of the capitals letters
def compareStr(str1, str2):
    if len(str1) == len(str2):
        cpt = 0
        while cpt < len(str1):
            if ord(str1[cpt]) == ord(str2[cpt]) or ord(str1[cpt]) == (ord(str2[cpt])+32) or ord(str1[cpt]) == (ord(str2[cpt])-32):
                cpt+=1
            else : return False
        return True
    return False

# Transform an element to a terminal friendly element
def transform(element):
    cpt = 0
    for i in element :
        if i == " " :
            element = element[:cpt] + '\ ' + element[cpt+1:]
            cpt+=1
        cpt+=1
    return element

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

def findAutheur(source, element, txt):
	result=""
	source = open(element,"r")
	titre = findTitle(source, element)
	print(titre)
	t = txt.split("Abstract",1)
	auteur = t[0].split(titre,1)
	for ligne in auteur:
		ligne = ligne[:-1]
		if not ligne.isin(titre) :
			result += ligne
	return result

def resultat(xml, tmp, result, element):
    os.chdir(tmp)
    source = open(element,"r")
    destination = open(result+'/'+element, "w") 
    
     
    print("Titre : " + findTitle(source, element), file = destination)
    source.close()
    

    nom = element[:-4] + '.pdf'
    print("\nnom du fichier : " + nom, file =destination)

    if xml :
        print(findAutheur(source), file = destination)
	
    source = open(element,"r")
    txt = source.read()
    a = findAutheur(source, element, txt)
    destination.write("\n\n\n auteur : ")
    for i in range(0,len(a)) :                                 
        destination.write(a[i])
    source.close()
    
    
    source = open(element,"r")
    txt = source.read()
    r = Abstract(txt)
    destination.write("\nResumé : ")
    for i in range(0,len(r)) :                                 
        destination.write(r[i]) 
        
    source.close()
    destination.close()


def xml(directory):  
    for element in os.listdir(directory):
        if element.endswith('.pdf'):
            if not os.path.exists(directory+"/xmlResultat"):
                os.mkdir(directory+"/xmlResultat")
            element = element.replace(".pdf", "")
            source = open(directory+"/resultToXml/"+element+".txt", "r")              
            f = open(directory+"/xmlResultat/"+element+".xml", "w")
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
            f.close()

def transmog(argv, directory):
    origin = "{0}/{1}".format(os.getcwd(), directory)
    xml = False
    if (argv[1] == "-t"):
        result = "{0}/{1}result".format(os.getcwd(), directory)
    else :
        result = "{0}/{1}resultToXml".format(os.getcwd(), directory)
        xml = True

    if os.path.exists(result):
        shutil.rmtree(result)
    os.mkdir(result)
    tmp = "{0}/{1}/tmp".format(os.getcwd(), directory)
    for element in os.listdir(tmp):
        if element.endswith('.txt'):
            resultat(xml, tmp, result, element)
    os.chdir(origin)
 
def pdf(directory):
    tmp = "{}/tmp".format(directory)
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.mkdir(tmp)
    for element in os.listdir(directory):
        if element.endswith('.pdf'):
            element = transform(element)
            titre = element[0:-4]
            a = "pdftotext -raw -nopgbrk -enc ASCII7 {0}/{1}/{2}  {0}/{1}/tmp/{3}.txt".format(os.getcwd(),directory, element, titre)
            os.system(a)

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
        if os.path.exists(directory) & os.path.isdir(directory):
            pdf(directory)
        else:
                print( "L'argument n'éxiste pas ou n'est pas un répertoire !")
                sys.exit(2)
        if argv[1] == "-t":
            transmog(argv, directory)
        elif argv[1] == "-x":
            transmog(argv, directory)
            os.chdir(current)
            xml(argv[2])
            os.chdir(current+"/"+directory)
            os.system("rm -r resultToXml")
        else :
            print("-option non reconnue :")
            print(" -t  version .txt")
            print(" -x  version .xml")
        #os.system("rm -r tmp")

                    

main(sys.argv)
