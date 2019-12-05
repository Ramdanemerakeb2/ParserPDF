# ParserPDF

Un parser qui récupère des informations d'un pdf normalisé de presse Scientifique et les écrit dans un fichier txt ou xml qui se trouvera dans un dossier à la position du pdf.

Language : python

utilise la fonction pdftotext avec les options : -raw -nopgbrk -enc ASCII7

Utilise les librairies python3 :

	shutil
	subprocess
	os
	os.path
	sys

how to use : python3 ParserPdf.py -option PathDuDossierContenantLePdf

options : 

	-t conversion en fichier txt

	-x conversion en fichier xml