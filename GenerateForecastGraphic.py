'''
 _______  _______  _______  _______ 
(  ____ \(       )(       )(  ___  )
| (    \/| () () || () () || (   ) |
| (__    | || || || || || || (___) |
|  __)   | |(_)| || |(_)| ||  ___  |
| (      | |   | || |   | || (   ) |
| (____/\| )   ( || )   ( || )   ( |
(_______/|/     \||/     \||/     \|
                                    
 _______          _________ _______ __________________
(  ____ \|\     /|\__   __/(  ____ \|__   __/\__   __/
| (    \/| )   ( |   ) (   | (    \/   ) (      ) (   
| |      | (___) |   | |   | (_____    | |      | |   
| |      |  ___  |   | |   (_____  )   | |      | |   
| |      | (   ) |   | |         ) |   | |      | |   
| (____/\| )   ( |___) (___/\____) |___) (___   | |   
(_______/|/     \|\_______/\_______)\_______/   )_( 

(c) Clinton Boys 2015

-----------------------
GenerateForecastGraphic.py
-----------------------

Generates the graphic containing the current Emma Chisit forecast. 
'''

import datetime
from PIL import Image
from pyx import *

composition = {'ALP': 55, 'COA': 90, 'IND': 3, 'PUP': 1, 'GRN': 1}
this_time = datetime.datetime.now()

def GenerateForecastGraphic(composition, this_time, filename):


	colors = {'ALP': color.rgb(1,10.0/255.0,10.0/255.0), 'COA': color.rgb(59.0/255.0,10.0/255.0,1), 'IND': color.rgb(171.0/255.0,171.0/255.0,171.0/255.0), 'PUP': color.rgb(247.0/255.0,1,10.0/255.0), 'GRN': color.rgb(8.0/255.0,242.0/255.0,0)}
	color_list = []
	for party in sorted(composition, key = composition.get):
		color_list.extend([colors[party] for i in range(composition[party])])

	current_day = str(this_time.day)
	current_month = str(this_time.month)
	current_year = str(this_time.year)
	current_time = this_time.time()
	current_hour = str(this_time.hour)
	current_minutes = '0'*(2-len(str(this_time.minute)))+str(this_time.minute)

	c = canvas.canvas()

	c.fill(path.rect(-0.5,-0.5,50.5,11.5), [color.rgb(116.0/255.0,138.0/255.0,117.0/255.0), color.transparency(0.6)])
	for i in range(0,150):
		c.fill(path.rect(2*(i%25),2*(i/25),1.5,0.5), [color_list[i]])

	im = bitmap.jpegimage('logo.jpg')
	bm = bitmap.bitmap(55,10,im ,width = 10, height = 2.5, compressmode = None)
	c.insert(bm)
	c.fill(path.rect(75,8,1,1), [color.rgb.white])
	c.fill(path.rect(-2,-2,1,1), [color.rgb.white])


	c.text(52, 8, r"Federal House of Representatives", [text.size.Huge])
	c.text(52, 6.5, r"Current forecast - updated %s/%s/%s at %s:%s"%(current_day, current_month, current_year, current_hour, current_minutes) ,[text.halign.boxleft, text.size.Huge])
	spacing = 0
	for party in sorted(composition, key = composition.get, reverse = True):
		c.text(52, 5.5-spacing, r"%s: %s"%(party, composition[party]), [text.size.LARGE])
		spacing += 1
	c.writePDFfile(filename)


GenerateForecastGraphic(composition, this_time, "style")