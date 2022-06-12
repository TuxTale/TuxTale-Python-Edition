from gmglobal import*
import json

timer = 0
autocon = 300

animation = {
	
	"events":[
		{
			"start": 0,
			"stop": 200,
			"autocon":{
				"right" : False,
				"left": False,
				"up" : False,
				"down" : False
			},
			"anim": None,
			"function": 0,
			"spawn": [
				{
					"entity": 0,
					"x" : 200,
					"y" : 200 
				},
				{
					"entity": 1,
					"x" : 200,
					"y" : 200 
				}
			]
		},
		{
			"start": 200,
			"stop": 400,
			"autocon":{
				"right" : False,
				"left": False,
				"up" : False,
				"down" : False
			},
			"anim": None,
			"function": 0,
			"spawn": [
				
			]
		},
		{
			"start": 400,
			"stop": 800,
			"autocon":{
				"right" : False,
				"left": False,
				"up" : False,
				"down" : False
			},
			"anim": None,
			"function": 0,
			"spawn": [
				
			]
		},
	]

}

for i in animation["events"]:
	if timer >= i["start"] and timer < i["stop"]:
		autocon = i["autocon"]
		print(autocon)
		

