ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.13.11"

lazy val root = (project in file("."))
  .settings(
    name := "json-to-graph"
  )

libraryDependencies ++= Seq(
  "io.github.neotypes" %% "neotypes-core" % "0.23.3",
  "org.mongodb.scala" %% "mongo-scala-driver" % "4.9.0"
)
