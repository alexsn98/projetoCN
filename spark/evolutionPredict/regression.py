from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression 

spark = SparkSession.builder.getOrCreate() 

data = spark.read.csv('./indicators.csv', header=True, inferSchema=True)

feature_columns = data.columns[:-1]

assembler = VectorAssembler(inputCols=feature_columns,outputCol="features") 

data_2 = assembler.transform(data) 

train, test = data_2.randomSplit([0.8, 0.2])

algo = LinearRegression(featuresCol="features", labelCol="2011") 

model = algo.fit(train) 

evaluation_summary = model.evaluate(test) 

print(evaluation_summary.meanAbsoluteError)
print(evaluation_summary.rootMeanSquaredError)
print(evaluation_summary.r2)

predictions = model.transform(test)

predictions.select(predictions.columns[48:]).show()