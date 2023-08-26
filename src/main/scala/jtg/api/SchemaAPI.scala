package jtg.api

import jtg.domain.Schema

class SchemaAPI() {
  private val globalSchema: scala.collection.mutable.Map[String, Schema] = scala.collection.mutable.Map();

  def get(item: String): Option[Schema] = {
    globalSchema.get(item);
  }

  def update(item: String, value: Schema) = {
    globalSchema.update(item, value);
  }
}
