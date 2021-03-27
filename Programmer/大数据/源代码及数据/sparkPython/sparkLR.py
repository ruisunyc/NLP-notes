# /root/tmp/sparkPython/sparkLR.py
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF,Tokenizer
if __name__ == '__main__':    
    spark=SparkSession.builder.master('local').appName('WordCountML').getOrCreate()
    training = spark.createDataFrame([(0,'a b c d spark',1.0),(1,'b d',0.0),(2,'spark f',1.0),(3,'hadd map',0.0)],['id','text','label'])
    tokenizer = Tokenizer(inputCol='text',outputCol='words')
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(),outputCol='features')
    lr = LogisticRegression(maxIter=10,regParam=0.001)
    pipeline = Pipeline(stages=[tokenizer,hashingTF,lr]) #构建流水线
    model = pipeline.fit(training) #训练
    test = spark.createDataFrame([(4,'spark'),(5,'b'),(6,'f spark '),(7,'apache hadoop')],['id','text'])
    prediction = model.transform(test) #预测
    select = prediction.select('id','text','probability','prediction')
    for row in select.collect():
        rid,text,probablity,predic =row
        print(rid,text,probablity,predic)