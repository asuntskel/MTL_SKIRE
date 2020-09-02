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
parc_index_list = [1,2,3,4,5,6,7,8,9,10,11,12]

second_xml = urllib.request.urlopen('http://montreal2.qc.ca/ski/donnees/conditions_neige.xml')
grand_parc_index_list = [1,2,3,4,5,6,7]

favoriteParkName = "Mont-Royal"
favoriteHighlightColor = "black"


mainUiWrapperSizeX = 325
mainUiWrapperSizeY = 130 + 50 * len(parc_index_list + grand_parc_index_list)
mainUiWrapper = Ui()
mainUiWrapper.geometry(str(mainUiWrapperSizeX)+"x"+str(mainUiWrapperSizeY))
mainUiWrapper.resizable(width = False, height = False)
mainUiWrapper.title("Ski à MTL")
mainUiWrapper.overrideredirect(1)

##############################################################
# Theme color init
themes = ["dark", "clear"]
chosenTheme = Theme(themes[0]) # write 'clear' or 'dark' for two themes...see theme.py
project_font_color = chosenTheme.font
project_bg_color = chosenTheme.bg

##############################################################
# Main window tkinter UI
parentTkFrame = Frame(mainUiWrapper, bd=30, bg=project_bg_color, height=mainUiWrapperSizeY)
parentTkFrame.pack(fill= "y", padx=2, pady=2)
bQuit = Button(parentTkFrame, bg=project_bg_color, fg=project_font_color, text="\te\tx\ti\tt\t", command = mainUiWrapper.quit)
bQuit.pack(pady=0, anchor="ne", fill="x")

##############################################################
class Parc:
	def __init__(self, name, state, date):
		self.name = name
		self.state = state
		self.date = date
		color = "black"

	def setColorByState(self): # this amazing function sets the color for the Park's newEntry in the tkinter window
		stringColorPalette = {
			"bad" : "red",
			"good" : "#379683",
			"excellent" : "#5CDB95",
			"null" : "gray",
			"fun" : "#050505"
		}

		if favoriteParkName in self.name:
			self.color = project_font_color
		elif "xcel" in self.state:
			self.color = stringColorPalette["excellent"]
		elif "on" in self.state:
			self.color = stringColorPalette["good"]
		elif "auvais" in self.state:
			self.color = stringColorPalette["bad"]
		elif "/" in self.state:
			self.color = stringColorPalette["null"]
		else:
			self.color = stringColorPalette["fun"]

	def checkForHighlight(self):
		# if this is our favoriteParkName parc, change
		# its bg color and activate the "x" filling

		if favoriteParkName in self.name: 
			return favoriteHighlightColor
		else:
			return project_bg_color


class ParsedXML:
	def __init__(self, url):
		self.url = url
		self.tree = ElementTree.parse(self.url)
		self.root = self.tree.getroot()

	def getParkInfo(self, parkType, ParkNumberIndex):
# dû aux différences inhérentes des fichiers XML qui peuvent être ici ajoutés
# voici alors un support pour les parcs d'arrondissement et les grands parcs.
# la méthode .build(True) return les résultats de parcs d'arrondissement,
# tandis que .build(False) return les résultats des grands parcs.
# dû aux architecture différentes, le XML des grands parcs est plus direct

		if parkType == petit_parc: #  Pour les Parcs d'arrondissement, ParkType n'a pas d'influence sur la recherche (root.findall)
		# ce statement est capable de trouver les résultats à l'intérieur d'une boucle
			self.names = self.root.findall("./piste/nom")
			self.states = self.root.findall("./piste/condition")
			self.dates = self.root.findall("./piste/arrondissement/date_maj")
			return self.names, self.states, self.dates

		elif parkType == grand_parc: # Pour les Grands Parcs, ParkNumberIndex = la valeur d'identification du parc
			self.names = (self.root.find((".//*[@id = '%s']/nom_fr") % ParkNumberIndex).text)
			self.states = (self.root.find((".//*[@id = '%s']/conditions/etat_general/ski/etat") % ParkNumberIndex).text)
			self.dates = (self.root.find((".//*[@id = '%s']conditions/date_maj") % ParkNumberIndex).text)
			return self.names, self.states, self.dates


##############################################################

parcs_en_arrondissement_XML = ParsedXML(xml)
grands_parcs_XML = ParsedXML(second_xml)

##############################################################
petit_parc = 1
grand_parc = 0
fill_x = "x"
fill_none = "none"

def returnParkInfos(parkType, ParkInformationIndex, ParkNumberIndex):
	if parkType == petit_parc:
		info = (parcs_en_arrondissement_XML.getParkInfo(True, 0))[ParkInformationIndex][ParkNumberIndex].text;
		return info
	elif parkType == grand_parc:
		info = (grands_parcs_XML.getParkInfo(False, ParkNumberIndex))[ParkInformationIndex]
		return info
	else:
		mainUiWrapper.quit()

def buildParkAndLabel(parkType, ParkNumberIndex, packSide):
	newEntry = Parc(
		name = returnParkInfos(parkType, 0, ParkNumberIndex), # 0-1-2 gets the name-state-date inside duild()
		state = returnParkInfos(parkType, 1, ParkNumberIndex),
		date = returnParkInfos(parkType, 2, ParkNumberIndex)
		)
	newEntry.setColorByState()
	newLabel = Label(parentTkFrame,
		font = "Helvetica 8",
		text = newEntry.name + "\n" + newEntry.state + "\n" + newEntry.date,
		fg = newEntry.color,
		bg = newEntry.checkForHighlight(),
		justify="left"
		)
	if favoriteParkName in newEntry.name:
		favoriteParkFillType = fill_x
	else:
		favoriteParkFillType = fill_none

	newLabel.pack(anchor="nw", pady=1, padx=10, fill= favoriteParkFillType, side=packSide)



for parc in parc_index_list:
	buildParkAndLabel(petit_parc, parc, "top")
for parc in grand_parc_index_list:
	buildParkAndLabel(grand_parc, parc, "bottom")

mainUiWrapper.mainloop()
