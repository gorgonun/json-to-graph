package jtg

import jtg.domain.Schema
import jtg.api.SchemaAPI
import org.mongodb.scala.{Document, MongoClient}

class JsonToGraph {
  val schemaApi = new SchemaAPI()

  def execute(doc: Document, name: String, threshold: Double): Unit = {
    val rootColumns = doc.map(_._1).toList
    schemaApi.get(name) match {
      case Some(schema) =>
        val diffColumns = schema.column_information.map(_._1) diff rootColumns
        val diffNewColumns = rootColumns diff schema.column_information.map(_._1)
        val diffColumnsSet = diffColumns.toSet
        val closeness = 1 - (diffColumns.size.toFloat / schema.column_information.length.toFloat)
        if (closeness >= threshold) {
          schemaApi.update(
            name,
            schema.copy(
              nodes = schema.nodes + (schema.last_id + 1),
              column_information = schema.column_information.map(information => {
                (information._1, information._2 && !diffColumnsSet.contains(information._1))
              }) ++ diffNewColumns.map((_, false)),
              last_id = schema.last_id + 1
            )
          )
        }
      case None =>
        schemaApi.update(
          name,
          Schema(
            name,
            rootColumns.map(x => (x, true)),
            Set(),
            0
          )
        )
    }
  }
}

object JsonToGraph {
  def main(args: Array[String]): Unit = {
    val threshold = 0.6;
    val mongoClient = MongoClient(sys.env("MONGODB_URL"))
    val collection = mongoClient.getDatabase("test").getCollection(sys.env("MONGODB_COLLECTION"))
    val docs = collection.find()
    val rootName = sys.env("MONGODB_COLLECTION");
    val job = new JsonToGraph()

    docs.foreach(doc => {
      job.execute(doc, rootName, threshold)
    })
  }
}
