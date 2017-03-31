d <- read.csv('singular_data_innings.csv')
list<-c()
for(i in c(1:nrow(d)))
{
  if(d$X[i]!='')
  {
    list=c(list,1)
  }
  else
  {
    list=c(list,0)
  }
}
k=1
for(i in list)
{
  d$Bool[k]=i;
  k=k+1;
}
#d <- rbind.data.frame(head(d),tail(d))
d <- d[-c(1:4,6,10:11)]
colnames(d)<-c("Bat","Bowl","Runs","Extra","Wicket")



batsmen <- unique.data.frame(d[i]$striker)
bowler <- unique.data.frame(d[i]$bowler)

batsmen$no_bowls=0
batsmen$runs=0
bastmen$wickets=0
bowler$runs=0
bowler$wickets=0
bowler$no_bowls=0
for(i in c(1:nrow(d)))
{
  batsmen[d[i]$batsman]$runs=batsmen[d[i]$batsman]$runs+d[i]$runs
  batsmen[d[i]$batsman]$no_bowls=batsmen[d[i]$batsman]$no_bowls+1
  batsmen[d[i]$batsmen]$wickets=batsmen[d[i]$batsmen]$wickets+d[i]$wickets
  bowler[d[i]$bowler]$wickets=bowler[d[i]$bowler]$wickets+d[i]$wickets
  bowler[d[i]$bowler]$wickets=bowler[d[i]$bowler]$wickets+d[i]$wickets
  bowler[d[i]$bowler]$no_bowls=bowler[d[i]$bowler]$no_bowls+1
}

for(i in c(i:nrow(d)))
{
  batsmen[d[i]$batsman]$str=batsmen[d[i]$batsman]$runs/batsmen[d[i]$batsman]$no_balls
  batsmen[d[i]$batsman]$avg=batsmen[d[i]$batsman]$runs/batsmen[d[i]$batsman]$wickets
  bowler[d[i]$bowler]$avg=bowler[d[i]$bowler]$wickets/bowler[d[i]$bowler]$no_balls
  bowler[d[i]$bowler]$eco=bowler[d[i]$bowler]$runs/bowler[d[i]$bowler]$no_balls
}

write.csv(batsmen,"bat.csv")
write.csv(bowler,"bowl.csv")