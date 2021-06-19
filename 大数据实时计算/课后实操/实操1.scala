import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.time.Time

object Main {
  val target="b"
//字符串中含b的个数
  def chCount(str: String):Int = {
    val string = str
    val count = string.count(_ == 'b')
    return count
  }

  def main(args: Array[String]) {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    //Linux or Mac:nc -l 9999
    //Windows:nc -l -p 9999
    val text = env.socketTextStream("localhost", 9999)
    val stream = text.flatMap {
      _.toLowerCase.split("\\W+") filter {
        _.contains(target)
      }
    }.map {
      ("发现目标："+_)
    }
    stream.print()
    val charCountStream = text.flatMap{
      _.toLowerCase.split("\\W+") filter {
        _.contains(target)
      }
    }
    var sum = charCountStream.map (item =>
      chCount(item)
    )
      .timeWindowAll(Time.seconds(60),Time.seconds(10)) // 定义了一个滑动窗口，窗口大小为60秒，每10秒滑动一次
      .sum(0)
    sum.print()
    env.execute("Window Stream WordCount")
  }
}