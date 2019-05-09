import org.apache.spark.{SparkContext, SparkConf}
object a {
  def main(args:Array[String]): Unit ={
    val conf = new SparkConf().setAppName("WordCount").setMaster("local")
    val sc = new SparkContext(conf)
    val js=sc.textFile("D:/project/spark_TFIDF/資治通鑒.txt")
    val jp_double=js.flatMap( x=>x.split("。")).flatMap(x=>x.split("，")).flatMap (x=>x.split(" ")).filter( x=>x!="").flatMap(x=>{for(i<-0 until x.length-1) yield (x(i)+","+x(i+1),1)})
    val frame=spark.createDataFrame(jp_double)
    frame.registerTempTable("stat")
    val order=spark.sql("select * from stat order by _2  ")
    order.show(100)
  }

}
