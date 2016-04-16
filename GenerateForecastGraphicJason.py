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
import pandas as pd
import datetime
from PIL import Image
import collections
from pyx import *

composition_frame = pd.read_csv('current_forecast.csv')

composition = {}
for i in range(0,len(composition_frame)):
	try:
		composition[composition_frame['winner'].iloc[i]] += 1
	except KeyError:
		composition[composition_frame['winner'].iloc[i]] = 1

composition['aALP'] = composition.pop('ALP')
composition['bIND'] = composition.pop('IND')
try:
	composition['cPUP'] = composition.pop('PUP')
except KeyError:
	pass
composition['dKAP'] = composition.pop('KAP')
composition['eGRN'] = composition.pop('GRN')
composition['zCOA'] = composition.pop('COA')

#composition = {'ALP': 55, 'COA': 90, 'IND': 3, 'PUP': 1, 'GRN': 1}
this_time = datetime.datetime.now() - datetime.timedelta(hours = -9)

from_svg = open('emmagraphic5.svg').readlines()
circles = []
for item in from_svg:
	if item[0:7] == '<circle':
		x = float(item.split('cx="')[1].split('"')[0])
		y = float(item.split('cy="')[1].split('"')[0])
		r = float(item.split('r="')[1].split('"')[0])
		circles.append([x,y,r])

numbers_map_old = {3:0, 2:1, 1:2, 0:3, 76:4,
			   8:5, 7:6, 6:7, 5:8, 4:9,
			   13:10, 12:11, 11:12, 10:13, 9:14,
			   18:15, 17:16, 16:17, 15:18, 14:19,
			   23:20, 22:21, 21:22, 20:23, 19:24,
			   28:25, 27:26, 26:27, 25:28, 24:29,
			   33:30, 32:31, 31:32, 30:33, 29:34,
			   38:35, 37:36, 36:37, 35:38, 34:39,
			   42:40, 41:41, 40:42, 39:43, 117:44,
			   43:45, 47:46, 46:47, 45:48, 44:49, 51:50,
			   58:51, 57:52, 56:53, 55:54, 48:55, 52:56,
			   64:57, 63:58, 62:59, 61:60, 60:61, 59:62, 49:63,
			   75:64, 74:65, 73:66, 72:67, 71:68, 70:69,
			   69:70, 68:71, 67:72, 66:73, 65:74, 139:75, 140:76, 141:77, 142:78, 143:79,
			   144:80, 145:81, 146:82, 147:83, 148:84, 149:85,
			   50:86, 133:87, 134:88, 135:89, 136:90, 137:91, 138:92,
			   54:93, 128:94, 129:95, 130:96, 131:97, 132:98,
			   53:99, 124:100, 125:101, 126:102, 127:103, 123:104,
			   118:105, 119:106, 120:107, 121:108, 122:109,
			   112:110, 113:111, 114:112, 115:113, 116:114,
			   107:115, 108:116, 109:117, 110:118, 111:119,
			   102:120, 103:121, 104:122, 105:123, 106:124,
			   97:125, 98:126, 99:127, 100:128, 101:129,
			   92:130, 93:131, 94:132, 95:133, 96:134,
			   87:135, 88:136, 89:137, 90:138, 91:139,
			   82:140, 83:141, 84:142, 85:143, 86:144,
			   77:145, 78:146, 79:147, 80:148, 81:149}

numbers_map = dict([[v,k] for k,v in numbers_map_old.items()])


def GenerateForecastGraphic(composition, this_time, filename):


	colors = {'aALP': color.rgb(1,10.0/255.0,10.0/255.0), 'bIND': color.rgb(171.0/255.0,171.0/255.0,171.0/255.0), 'cPUP': color.rgb(247.0/255.0,1,10.0/255.0), 'eGRN': color.rgb(8.0/255.0,242.0/255.0,0), 'dKAP': color.rgb(1,166.0/255.0,0), 'zCOA': color.rgb(59.0/255.0,10.0/255.0,1)}
	color_list = []
	for party in collections.OrderedDict(sorted(composition.items())):#sorted(composition, key = composition.get):
		color_list.extend([colors[party] for i in range(composition[party])])

	current_day = str(this_time.day)
	current_month = str(this_time.month)
	current_year = str(this_time.year)
	current_time = this_time.time()
	current_hour = str(this_time.hour)
	current_minutes = '0'*(2-len(str(this_time.minute)))+str(this_time.minute)



	c = canvas.canvas()

	#c.fill(path.rect(-0.5,-0.5,50.5,11.5), [color.rgb(116.0/255.0,138.0/255.0,117.0/255.0), color.transparency(0.6)])
	for i in range(0,len(circles)):
		c.fill(path.circle(circles[numbers_map[i]][0]/150.0, circles[numbers_map[i]][1]/150.0, circles[numbers_map[i]][2]/150.0), [color_list[i]])
		#c.text(circles[i][0]/10.0, circles[i][1]/10.0, str(i), [text.size.Huge])
	# for i in range(0,150):
	# 	c.fill(path.rect(2*(i%25),2*(i/25),1.5,0.5), [color_list[i]])

	# # im = bitmap.jpegimage('logo.jpg')
	# # bm = bitmap.bitmap(55,10,im ,width = 10, height = 2.5, compressmode = None)
	# # c.insert(bm)
	c.fill(path.rect(6,4,1,1), [color.rgb.white])
	#c.fill(path.rect(-2,-2,1,1), [color.rgb.white])


	# c.text(7, 3.1, r"Federal House of Representatives", [text.size.small])
	# c.text(7, 2.7, r"Current forecast - updated %s/%s/%s at %s:%s"%(current_day, current_month, current_year, current_hour, current_minutes) ,[text.halign.boxleft, text.size.small])
	spacing = 0
	for party in sorted(composition, key = composition.get, reverse = True):
		c.text(2, 2.6-spacing, r"%s: %s"%(str(party)[1:], composition[party]),[text.size.small])
		spacing += 0.4
	c.writePDFfile(filename)


GenerateForecastGraphic(composition, this_time, "style")