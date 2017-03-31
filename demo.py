import pandas as pd
import random
import webbrowser
import glob
import time
print('Select team1:');team1_name=input() #ex. rcb,  mi ,  rcb,  srh, rcb 
print('Select team2:');team2_name=input() #ex. mi,   kkr,  srh,  mi,  kkr
team_lineup=pd.read_csv( 'members/' + team1_name + 'vs' + team2_name+ '.csv')
team1 = list(map(lambda x:x.strip(),team_lineup.team1))
team2 = list(map(lambda x:x.strip(),team_lineup.team2))
f = open("output.html", 'w')
url = "file:///home/siddharths2710/Desktop/demo/output.html"
f.write("<!DOCTYPE html>\n<html>\n<head>\n<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\nwidth: 100%;\n}")
f.write("td, th {\nborder: 1px solid #dddddd;\ntext-align: left;\npadding: 8px;\n}\n")
f.write("\ntr:nth-child(even) {\nbackground-color: #dddddd;\n}\n</style>\n</head>\n<body>\n")
batsman_cluster_files = sorted(glob.glob("Clusters/Bat_Cluster/*.csv"))
bowler_cluster_files = sorted(glob.glob("Clusters/Bowl_Cluster/*.csv"))

cluster_probs = pd.read_csv('cluster_probabilities.csv')
cumulative_probs = pd.DataFrame(columns=['BatclustNo','BowlclustNo','0s', '1s', '2s', '3s', '4s',  '6s','Out'])
	

bat_dict = {};ball_dict = {}
for i in range(len(batsman_cluster_files)):
	dfbat = pd.read_csv(batsman_cluster_files[i])
	dfbowl = pd.read_csv(bowler_cluster_files[i])
	for j in range(len(dfbat)):
		batsman_name = dfbat.loc[j].Name.strip()
		bat_dict[batsman_name] = i
	for j in range(len(dfbowl)):
		bowler_name = dfbowl.loc[j].Name.strip()
		ball_dict[bowler_name] = i
BatmanNames = list(bat_dict.keys())
BowlerNames = list(ball_dict.keys())

for i in range(len(cluster_probs)):
	cumulative_probs.loc[i] = [None for n in range(9)]
	cumulative_probs.loc[i].BatclustNo = cluster_probs.loc[i].BatclustNo
	cumulative_probs.loc[i].BowlclustNo = cluster_probs.loc[i].BowlclustNo
	cumulative_probs.loc[i]['0s'] = float(cluster_probs.loc[i]['0s'])
	cumulative_probs.loc[i]['1s'] = float(cluster_probs.loc[i]['1s']) + float(cluster_probs.loc[i]['0s'])
	cumulative_probs.loc[i]['2s'] = float(cluster_probs.loc[i]['2s']) + float(cumulative_probs.loc[i]['1s'])
	cumulative_probs.loc[i]['3s'] = float(cluster_probs.loc[i]['3s']) + float(cumulative_probs.loc[i]['2s'])
	cumulative_probs.loc[i]['4s'] = float(cluster_probs.loc[i]['4s']) + float(cumulative_probs.loc[i]['3s'])
	cumulative_probs.loc[i]['6s'] = float(cluster_probs.loc[i]['6s']) + float(cumulative_probs.loc[i]['4s'])
	cumulative_probs.loc[i].Out = 1

def optimize_name(n,x):
	if x == 1:
		batsman_name = n
		batsman_last_name = batsman_name.split()[-1]
		for lbat in range(len(BatmanNames)):
			if batsman_last_name in BatmanNames[lbat] and (batsman_name[0] == BatmanNames[lbat][0] or batsman_name[1] == BatmanNames[lbat][0]):
				batsman_name = BatmanNames[lbat];break
		return bat_dict.get(batsman_name,2)
	else:
		bowler_name =  n
		bowler_last_name = bowler_name.split()[-1]
		for lbowl in range(len(BowlerNames)):
			if bowler_last_name in BowlerNames[lbowl] and (bowler_name[0] == BowlerNames[lbowl][0] or bowler_name[1] == BowlerNames[lbowl][0]):
				bowler_name = BowlerNames[lbowl];break
		return ball_dict.get(bowler_name,3)

def random_score(batsman,bowler):
	ptr = random.random()
	prob = cumulative_probs.loc[cumulative_probs['BatclustNo'] == batsman].loc[cumulative_probs['BowlclustNo'] == bowler]
	if 0.05 <ptr <= float(prob['0s']):
		return 0
	elif  float(prob['0s']) < ptr <= float(prob['1s']):
		return 1
	elif float(prob['1s']) < ptr <= float(prob['2s']):
		return 2
	elif float(prob['2s']) < ptr <= float(prob['3s']):
		return 3
	elif float(prob['3s']) < ptr <= float(prob['4s']):
		return 4
	elif float(prob['4s']) < ptr <= float(prob['6s']):
		return 6
	else:
		if ptr < 0.95:
			return 99
		return -1	

def batsman_cluster_no(batsman):
	return bat_dict.get(batsman,optimize_name(batsman,1))
def bowler_cluster_no(bowler):
	return ball_dict.get(bowler,optimize_name(bowler,0))

def match_simulation(t1, t2,goal = 10000): #Goal is control between innings1 and innings2
	f.write("<tr><th>Batsman</th><th>Non-Striker</th><th>Bowler</th><th>Overs</th><th>Score</th><th>Commentary</th></tr>")
	Commentary = ""
	rand_prob = 0
	striker=t1[0]
	runner=t1[1]
	bowler=t2[-1]
	count=2
	nextBatsman=2
	wickets=0
	over=0
	runs = 0
	ball = 0
	while(wickets<10 and over<20):
		ball = 0
		while(ball<6 and wickets<10):
			Commentary = ""
			score=random_score(batsman_cluster_no(striker),bowler_cluster_no(bowler))
			if(score==99):	
				runs += 1
				rand_prob = random.random()
				if rand_prob <= 0.25:
					Commentary = "No Ball"
				elif rand_prob <= 0.5:
					Commentary = "Leg Bye"
				else:
					Commentary = "Wide"
			else:
				if(score == -1):
					wickets += 1
					rand_prob = random.random()
					if rand_prob <= 0.25:
						Commentary = "Run Out!"
					elif rand_prob <= 0.5:
						Commentary = "Bowled!!"
					else:
						Commentary = "Caught!"
					striker=t1[nextBatsman]
					nextBatsman = (nextBatsman + 1)%11
				else:
					if score == 0:
						Commentary = "no runs"
					elif score == 1:
						Commentary = "single"
					elif score == 4:
						Commentary = "Its a Four!!"
					elif score == 6:
						Commentary = "A huge Six!!"
					elif score == 3:
						Commentary = "Three runs"
					else:
						Commentary = str(score) + " runs"
					runs+=score
					if(score==1 or score==3):
						(striker,runner) = (runner,striker)
				f.write("<tr><td>" + striker +"</td><td>"+ runner +"</td><td>"+bowler+"</td><td>"+str(over)+'.'+str(ball)+"</td><td>"+ str(runs) +'/'+ str(wickets) +"</td><td>"+Commentary+"</td></tr>")
				if score != 99:
					ball +=  1
				if runs > goal:
					return runs,wickets
		(striker,runner) = (runner,striker)
		over += 1
		bowler = t2[-1*count]
		count = (count+1)%5 + 1
	return (runs,wickets)

def match_results(runs1,runs2,wickets1,wickets2,name1,name2):
	name1 = name1.upper()
	name2 = name2.upper()
	print(name1 + ':',str(runs1) + '/'+str(wickets1))
	print(name2 + ':',str(runs2) + '/'+str(wickets2))
	s = ""
	if runs1>runs2:
		if wickets1<wickets2:
			s =  name1 + " wins by "+ str(wickets2 - wickets1) +" wickets"
		else:
			s = name1 + " wins by "+str(runs1-runs2)+" runs"
	elif runs2>runs1:
		if wickets2<wickets1:
			s = name2 + " wins by "+ str(wickets1 - wickets2) +" wickets"
		else:
			s = name2 + " wins by " + str(runs2-runs1) + " runs"
	else:
		s = "Match Tied"
	print(s)
	f.write("<br><hr><br><h1>"+ s +"</h1><br>")

f.write("<h2>1st Innings - 1st Innings Summary</h2><br><hr><br><table>")
r1,w1 = match_simulation(team1, team2)

f.write("</table><br><hr><br>")

f.write("<h2>2nd Innings - 2nd Innings Summary</h2><br><hr><br><table>")
r2,w2 = match_simulation(team2, team1,r1)
f.write("</table>")

match_results(r1,r2,w1,w2,team1_name,team2_name)
f.write("</body></html>")
f.close()
time.sleep(7)
webbrowser.open(url,new=2)