package big.data.analyse.tfidf

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession

object TF_IDF {
  Logger.getLogger("org").setLevel(Level.WARN)
  def main(args: Array[String]) {
    val spark = SparkSession
      .builder()
      .appName("TF_IDF")
      .master("local[2]")
      .config("spark.sql.warehouse.dir", filename).getOrCreate()
    val sc = spark.sparkContext
    /**
      * 计算TF
      */
    val tf = sc.textFile("src/big/data/analyse/tfidf/TF.txt")
      .map(row => row.replace(",", " ").replace(".", " ").replace("  ", " ")) // 数据清洗
      .flatMap(row => row.split(" ")) // 拆分
      .map(row => (row, 1.0))
      .reduceByKey(_+_)

    val tfSize = tf.map(row => row._2).sum() // 计算总词数

    val tfed = tf.map(row => (row._1, row._2 / tfSize.toDouble)) //求词频
    println("TF：")
    tfed.foreach(println)

    /**
      * 计算IDF
      */
    val idf_0 = tf.map(row => (row._1, 1.0))
    println("加载IDF1文件数据。。。")
    val idf_1 = sc.textFile("src/big/data/analyse/tfidf/IDF1.txt")
      .map(row => row.replace(",", " ").replace(".", " ").replace("  ", " "))
      .flatMap(row => row.split(" "))
      .map(row => (row, 1.0))
      .reduceByKey(_+_)
      .map(row => (row._1, 1.0))

    println("加载IDF2文件数据。。。")
    val idf_2 = sc.textFile("src/big/data/analyse/tfidf/IDF2.txt")
      .map(row => row.replace(",", " ").replace(".", " ").replace("  ", " "))
      .flatMap(row => row.split(" "))
      .map(row => (row, 1.0))
      .reduceByKey(_+_)
      .map(row => (row._1, 1.0))

    /**
      * 整合语料库数据
      */
    val idf = idf_0.union(idf_1).union(idf_2)
      .reduceByKey(_+_)
      .map(row => (row._1, 3 / row._2))
    println("IDF：")
    idf.foreach(println)

    /**
      * 关联TF和IDF，计算TF-IDF
      */
    println("TF-IDF：")
    tfed.join(idf).map(row => (row._1, (row._2._1 * row._2._2).formatted("%.4f")))
      .foreach(println)
  }
}