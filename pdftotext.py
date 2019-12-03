import shutil   #pour suprimmer recursivement
import subprocess as sp #commande 
import os       #commande de base
import os.path  #le path du program
import sys      #argument 

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
    cpt = 0
    for i in element :
        if i == " " :
            element = element[:cpt] + '\ ' + element[cpt+1:]
            cpt+=1
        cpt+=1
    return element

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
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.mkdir(tmp)
    for element in os.listdir(arg):
        if element.endswith('.pdf'):
            element = transformEintoE(element)
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
            resultat(source,destination,element)
            source.close()
            destination.close()
    os.chdir(origin)
          

def xml(arg):  
    for element in os.listdir(arg):
        if element.endswith('.pdf'):
            if not os.path.exists(arg+"/xmlResultat"):
                os.mkdir(arg+"/xmlResultat")
            element = element.replace(".pdf", "")
            source = open("Papersresultat/"+element+".txt", "r")              
            f = open(arg+"/xmlResultat/"+element+".xml", "w")
            i=1
            for line in source:
                if i == 1:
                    t = line
                    t = t[8:]
                if i == 3:
                    p = line
                    p = p[17:]
                if i == 5:
                    a = line
                    a = a[9:]
                i+=1
            f.write("<article>\n")          
            f.write("\t<preamble>"+p+"</preamble>\n")
            f.write("\t<titre>"+t+"</titre>\n")
            f.write("\t<abstract>"+a+"</abstract>\n")
            f.write("</article>")            
            
def main(argv):               
    if len(argv) != 3:
        print("Deux arguments attendus !")
        print(argv)
        sys.exit(2)
    else:
        current = os.getcwd()     
        if len(argv) == 3:
            if argv[1] == "-t":
                if os.path.exists(argv[2]) & os.path.isdir(argv[2]):
                    pdftotext(argv[2])
                    transmog(argv[2])
                    #os.system("rm -r tmp")
                else:
                    print( "L'argument n'éxiste pas ou n'est pas un répertoire !")
                    sys.exit(2)
            elif argv[1] == "-x":
                if os.path.exists(argv[2]) & os.path.isdir(argv[2]):
                    xml(argv[2])




main(sys.argv)