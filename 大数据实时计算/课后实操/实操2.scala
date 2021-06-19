import java.util.{Properties, UUID}
import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer010
import scala.collection.immutable.HashMap


object Main {
  /**
   * 输入的主题名称
   */
  val inputTopic = "mn_buy_ticket_1"
  /**
   * kafka地址
   */
  val bootstrapServers = "bigdata35.depts.bingosoft.net:29035,bigdata36.depts.bingosoft.net:29036,bigdata37.depts.bingosoft.net:29037"


  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
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
    var map = new HashMap[String,Int]
    inputKafkaStream.map(x=>{
      val destinations=x.split(",")(3)
      val city=destinations.substring(15,destinations.length-1)
      //println(city)
      if(map.exists(_._1==city)){
        val t=map(city)+1
        map-=city
        map+=(city->t)
      }
      else {
        map+=(city->1)
      }
      println("目的地数量前5：")
      map.toList.sortBy(-_._2).take(5).foreach{
        case (key, value) => println(key + value)
      }
    })
    env.execute()
  }
}