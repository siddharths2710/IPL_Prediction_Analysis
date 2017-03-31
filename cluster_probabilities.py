import pandas as pd
import glob
cprobs = pd.DataFrame(columns=[ '0s', '1s', '2s', '3s', '4s',  '6s','Out','Batcluster','Bowlcluster'])
bat_cluster_files = sorted(glob.glob("Clusters/Bat_Cluster/*.csv"))
bowl_cluster_files = sorted(glob.glob("Clusters/Bowl_Cluster/*.csv"))
prob = pd.read_csv('singular_data_innings_prob.csv')


#Dict for lookups
Batsman_dict = {}
Bowler_dict = {}
for i in range(len(bat_cluster_files)):
	Batsman_file = pd.read_csv(bat_cluster_files[i])
	Bowler_file = pd.read_csv(bowl_cluster_files[i])
	for j in range(len(Batsman_file)):
		Batsman_dict[Batsman_file.loc[j].Name.strip()] = Batsman_file.loc[j].clustno
	for j in range(len(Bowler_file)):
		Bowler_dict[Bowler_file.loc[j].Name.strip()] = Bowler_file.loc[j].clustno


Batsman_dict_names = list(Batsman_dict.keys())
Bowler_dict_names = list(Bowler_dict.keys())
# Batsman_dict_names & Bowler_dict_names for optimization

index=0
print(prob.index)
for l in range(len(prob)):
	batsman_name = prob.loc[l].Name.strip()
	batsman_first_name = batsman_name.split()[-2]	
	batsman_last_name = batsman_name.split()[-1]
	for indexBat in range(len(Batsman_dict_names)):
		if batsman_last_name in Batsman_dict_names[indexBat] and (batsman_name[0] == Batsman_dict_names[indexBat][0] or batsman_name[1] == Batsman_dict_names[indexBat][0] or batsman_name[2] == Batsman_dict_names[indexBat][0]):
			batsman_name = Batsman_dict_names[indexBat];break
		elif batsman_last_name in Batsman_dict_names[indexBat]  and batsman_first_name in Batsman_dict_names[indexBat]  :
			batsman_name = Batsman_dict_names[indexBat];break
	print(l	)
	bowlname =  prob.loc[l].Bowler.strip()
	bowlfirstname = bowlname.split()[0] 	
	bowlastname = bowlname.split()[-1]
	for lbowl in range(len(Bowler_dict_names)):
		if bowlastname in Bowler_dict_names[lbowl] and (bowlname[0] == Bowler_dict_names[lbowl][0] or bowlname[1] == Bowler_dict_names[lbowl][0] or bowlname[2] == Bowler_dict_names[lbowl][0]):
			bowlname = Bowler_dict_names[lbowl];break;
		elif bowlastname in Bowler_dict_names[lbowl] and bowlfirstname in Bowler_dict_names[lbowl]:
			bowlname = Bowler_dict_names[lbowl];break;
	cprobs.loc[index] = [None for n in range(9)]
	cprobs.loc[index]['0s'] = prob.loc[l]['0s']
	cprobs.loc[index]['1s'] = prob.loc[l]['1s']
	cprobs.loc[index]['2s'] = prob.loc[l]['2s']
	cprobs.loc[index]['3s'] = prob.loc[l]['3s']
	cprobs.loc[index]['4s'] = prob.loc[l]['4s']
	cprobs.loc[index]['6s'] = prob.loc[l]['6s']
	cprobs.loc[index].Out = prob.loc[l].Out
	cprobs.loc[index].Batcluster = Batsman_dict[batsman_name]
	cprobs.loc[index].Bowlcluster = Bowler_dict[bowlname]
	#print(batsman_name,bowlname,Batsman_dict[batname],Bowler_dict[bowlname],index)	
	index += 1
cprobs.groupby(['Batcluster','Bowlcluster']).mean().to_csv('cluster_probabilities1.csv')
