from tkinter import *
import tkinter
from ui import Ui
from theme import Theme
from xml.etree import ElementTree
import urllib.request

###### this should be the newest version...###################
##############################################################
# opening xml into var for parser
xml = urllib.request.urlopen('http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_PISTE_SKI.xml')
second_xml = urllib.request.urlopen('http://montreal2.qc.ca/ski/donnees/conditions_neige.xml')

##############################################################
# list index choice for parcs to be displayed
parc_index_list = [1,2,3,4,5,6,7,8,9,10,11,12]
grand_parc_index_list = [1,2,3,4,5,6,7]
favorite = "Mont-Royal"

##############################################################
# main UI sizing/base parameters
size_x = 325
size_y = 130 + 50 * len(parc_index_list + grand_parc_index_list)
ui = Ui()
ui.geometry(str(size_x) + "x" + str(size_y))
ui.resizable(width = False, height = False)
ui.title("Mtl en ski")
ui.overrideredirect(1)

##############################################################
# Theme color init
chosenTheme = Theme("dark") # write 'clear' or 'dark' for two themes...see theme.py
font = chosenTheme.font
bg = chosenTheme.bg

##############################################################
# Main window tkinter UI
f1 = Frame(ui, bd=30, bg=bg, height=size_y)
f1.pack(fill= "y", padx=2, pady=2)
bQuit = Button(f1, bg=bg, fg=font, text="\te\tx\ti\tt\t", command = ui.quit)
bQuit.pack(pady=0, anchor="ne", fill="x")

##############################################################
class Parc:
	def __init__(self, name, state, date):
		self.name = name
		self.state = state
		self.date = date
		color = "black"



	def colorVerify(self): # this amazing function sets the color for the Park's newEntry in the tkinter window
		if favorite in self.name:
			self.color = font
		elif "xcel" in self.state:
			self.color = "#5CDB95"
		elif "on" in self.state:
			self.color = "#379683"
		elif "auvais" in self.state:
			self.color = "red"
		elif "/" in self.state:
			self.color = "gray"
		else:
			self.color = "#050505"

	def styleVerify(self, selector):
		# if this is our favorite parc, change
		# its bg color and activate the "x" filling

		if favorite in self.name: 
			if selector == "color":
				return "#000000"
			else:
				return selector
		else:
			return bg


class Parsed:
	def __init__(self, url):
		self.url = url
		self.tree = ElementTree.parse(self.url)
		self.root = self.tree.getroot()

	def build(self, switchBool, ParkNumberIndex):
# dû aux différences inhérentes des fichiers XML qui peuvent être ici ajoutés
# voici alors un support pour les parcs d'arrondissement et les grands parcs.
# la méthode .build(True) return les résultats de parcs d'arrondissement,
# tandis que .build(False) return les résultats des grands parcs.
# dû aux architecture différentes, le XML des grands parcs est plus direct

		if switchBool == True: #  Pour les Parcs d'arrondissement, i = rien.
		# ce statement est capable de trouver les résultats à l'intérieur d'une boucle
			self.names = self.root.findall("./piste/nom")
			self.states = self.root.findall("./piste/condition")
			self.dates = self.root.findall("./piste/arrondissement/date_maj")
			return self.names, self.states, self.dates

		elif switchBool == False: # Pour les Grands Parcs, ParkNumberIndex = la valeur d'identification du parc
			self.names = (self.root.find((".//*[@id = '%s']/nom_fr")% ParkNumberIndex).text)
			self.states = (self.root.find((".//*[@id = '%s']/conditions/etat_general/ski/etat")% ParkNumberIndex).text)
			self.dates = (self.root.find((".//*[@id = '%s']conditions/date_maj")% ParkNumberIndex).text)
			return self.names, self.states, self.dates


##############################################################

urlParsed = Parsed(xml)
urlParsed2 = Parsed(second_xml)

##############################################################
petit_parc = 1
grand_parc = 0


def getInfo(ParkType, ParkInformationIndex, ParkNumberIndex):
	if ParkType == petit_parc:
		info = (urlParsed.build(True, 0))[ParkInformationIndex][ParkNumberIndex].text;
		return info
	elif ParkType == grand_parc:
		info = (urlParsed2.build(False, ParkNumberIndex))[ParkInformationIndex]
		return info
	else:
		ui.quit()

def labelAndPack(ParkType, ParkNumberIndex, packside):
	newEntry = Parc(
		name = getInfo(ParkType, 0, ParkNumberIndex), # 0-1-2 gets the name-state-date inside duild()
		state = getInfo(ParkType, 1, ParkNumberIndex),
		date = getInfo(ParkType, 2, ParkNumberIndex)
	)
	newEntry.colorVerify()
	newLabel = Label(f1,
		font = "Helvetica 8",
		text = newEntry.name + "\n" + newEntry.state + "\n" + newEntry.date,
		fg = newEntry.color,
		bg = newEntry.styleVerify("color"),
		justify="left"
		)
	if favorite in newEntry.name:
		fav_fill = "x"
	else:
		fav_fill = "none"

	newLabel.pack(anchor="nw", pady=1, padx=10, fill= fav_fill, side=packside)



### actual park label building loops
for i in parc_index_list:
	labelAndPack(1, i, "top")

for i in grand_parc_index_list:
	labelAndPack(0, i, "bottom")

''' 
The projet is basically a XML parser, with some xml <tags> handling. All this is in order to
acquire some informations about ski conditions in Montreal. Two main files are provided by 
the city online, but their architecture is very different. The flow of the code is frail, but
does the job.

Basically, I use the build() method of Parsed to acquire data in order to fill Parc objects.
An arbitrary list of integers represent the number of <parcs> in the XML given, manually counted.
Upon building the tkinter labels for the main window UI, it iterates through both list, one after the other,
and for each number, finds the Parsed data to create Parc objects. Some awkward coloring is done in order to ease the eye. 

two themes exist : clear and dark. I don't recommend clear
'''
ui.mainloop()
