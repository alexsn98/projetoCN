from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression 

def train_regression(file_name):
  spark = SparkSession.builder.getOrCreate() 

  data = spark.read.csv(file_name, header=True, inferSchema=True)

  feature_columns = data.columns[1:-1]
  lastYear = data.columns[-1]

  assembler = VectorAssembler(inputCols=feature_columns, outputCol="features") 

  data_2 = assembler.transform(data) 
  # train, test = data_2.randomSplit([0.8, 0.2])

  algo = LinearRegression(featuresCol="features", labelCol=lastYear) 
  model = algo.fit(data_2) 

  predictions = model.transform(data_2)
  predictions.select(["countries","2012", "2013", "prediction"]).show()

  return model

def save_in_db():
  pass