package jtg.domain

case class Schema(table_id: String, column_information: List[(String, Boolean)], nodes: Set[Int], last_id: Int)
