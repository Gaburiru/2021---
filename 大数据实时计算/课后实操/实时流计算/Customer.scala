import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.api.scala.createTypeInformation
import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer010

import java.text.{DateFormat, SimpleDateFormat}
import java.util.{Date, Properties, UUID}

object Consumer {
  val accessKey = "8FA33F5E68860EEAA159"
  val secretKey = "WzZEQjk5NkZDOUJBNUJEREFCQzAyNkVEMzBGQUEy"
  val endpoint = "http://scut.depts.bingosoft.net:29997"
  val bucket = "zhuolin"
  //上传文件的路径前缀
  val pastKeyPrefix = "upload/"
  //上传数据间隔 单位毫秒
  val period = 5000
  //输入的kafka主题名称
  val inputTopic = "zhuolin_topic"
  //kafka地址
  val bootstrapServers = "bigdata35.depts.bingosoft.net:29035,bigdata36.depts.bingosoft.net:29036,bigdata37.depts.bingosoft.net:29037"

  def main(args: Array[String]): Unit = {

    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(1)
    val kafkaProperties = new Properties()
    kafkaProperties.put("bootstrap.servers", bootstrapServers)
    kafkaProperties.put("group.id", UUID.randomUUID().toString)
    kafkaProperties.put("auto.offset.reset", "earliest")
    kafkaProperties.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
    kafkaProperties.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
    val kafkaConsumer = new FlinkKafkaConsumer010[String](inputTopic,
      new SimpleStringSchema, kafkaProperties)
    kafkaConsumer.setCommitOffsetsOnCheckpoints(true)
    val inputKafkaStream = env.addSource(kafkaConsumer)
    val out = inputKafkaStream.flatMap{
      _.split("\n") filter {
        _.contains("2019/10")
      }
    }

    out.writeUsingOutputFormat(new S3Writer(accessKey, secretKey, endpoint, bucket, pastKeyPrefix, period))
    env.execute()
  }

  def tranTimeToString(tm: String): String = {
    val fm = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
    val tim = fm.format(new Date(tm.toLong))
    tim
  }

  def TimeCompare(buyTime: String, constantTime: String): Boolean = {
    var flag = false
    val df: DateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
    try {
      val buy: Date = df.parse(buyTime)
      val constant: Date = df.parse(constantTime)

      val bs: Long = buy.getTime - constant.getTime
      if (bs < 0) {
        flag = true
      }
    }
    catch {
      case e: Exception => {
      }
    }
    flag
  }
}