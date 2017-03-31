import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.clustering.KMeans
import org.apache.spark.sql.functions._

object cluster_IPL {
  def main(args: Array[String]): Unit = {

        val data = sc.textFile("hdfs://localhost:50070/Big_Data_assgn/bat.csv") //and ball.csv
        val header = data.first
        
        val rows = data.filter(l => l != header) //remove header
         case class CC1(SLNO:String,Name:String,Avg:Double,SR:Double)
         val allSplit = rows.map(line => line.split(","))
        val allData = allSplit.map( p => CC1( p(0).toString,p(1).toString, p(2).trim.toDouble,p(3).trim.toDouble))
        val allDF = allData.toDF()
         val rowsRDD = allDF.rdd.map(r => (r.getString(0),r.getString(1), r.getDouble(2),r.getDouble(3)))
        rowsRDD.cache()
        //Pass what all to kmeans
        val vectors = allDF.rdd.map(r => Vectors.dense( r.getDouble(2),r.getDouble(3))) //AvgRR,SR for batsman and Econ,SR for bowler
        vectors.cache()
        //KMeans model with 5 clusters and 20 iterations
        val kMeansModel = KMeans.train(vectors, 5, 20)
        
        //Print the center of each cluster
        
        kMeansModel.clusterCenters.foreach(println)
        
        // Get the prediction from the model with the ID so we can link them back to other information
        val predictions = rowsRDD.map{r => (r._2, kMeansModel.predict(Vectors.dense(r._3, r._4) ))}
        
        val predDF = predictions.toDF("Name", "CLUSTER")
        
        val t = allDF.join(predDF, allDF.col("Name"))

  }
}

Batsman =>
select Name,CLUSTER from clustBat limit 20;
Name                 CLUSTER
"Aakash Chopra"         2      
"Aaron Finch"           0      
"AB de Villiers"        3      
"Abhimanyu Mithun"      2      
"Abhishek Jhunjhunwala" 1      
"Abhishek Nayar"        1      
"Abhishek Raut"         1      
"Abu Nechim"            4      
"Adam Gilchrist"        0      
"Adam Voges"            2      
"Aditya Dole"           4      
"Aditya Tare"           1      
"Adrian Barath"         1      
"Aiden Blizzard"        1      
"Ajinkya Rahane"        3      
"Ajit Agarkar"          0      
"Akshath Reddy"         1      
"Akshdeep Nath"         2      
"Albie Morkel"          1      
"Ambati Rayudu"         0 

Bowler =>
select Name,CLUSTER from clustBowl limit 20;

Name                 CLUSTER
"Aaron Finch"           1      
"Aavishkar Salvi"       0      
"Abhimanyu Mithun"      0      
"Abhishek Jhunjhunwala" 4      
"Abhishek Nayar"        0      
"Abu Nechim"            4      
"Adam Gilchrist"        1      
"Adam Milne"            1      
"Adam Zampa"            4      
"Aditya Dole"           1      
"Ajantha Mendis"        4      
"Ajinkya Rahane"        1      
"Ajit Agarkar"          2      
"Ajit Chandila"         4      
"Albie Morkel"          0      
"Alfonso Thomas"        3      
"Ali Murtaza"           3      
"Amit Mishra"           3      
"Amit Singh"            3      
"Amit Uniyal"           1 
