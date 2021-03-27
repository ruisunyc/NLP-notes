#/root/tmp/sparkPython/DecisionTreeClassifier.py
from pyspark.sql import SparkSession
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.linalg import Vector, Vectors
from pyspark.sql import Row
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer, HashingTF, Tokenizer



def f(x):
    # x列表
    rel = {}
    rel['features'] = Vectors.dense(float(x[0]), float(x[1]), float(x[2]), float(x[3]))
    rel['label'] = str(x[4])
    return rel


if __name__ == '__main__':
    spark = SparkSession.builder.master('local').appName('LogisticRegression').getOrCreate()
    
    data = spark.sparkContext.textFile('file:///root/tmp/sparkPython/data/iris.txt').map(lambda x: x.split('\t')).map(
        lambda p: Row(**f(p))).toDF()
    labelIndexer = StringIndexer().setInputCol('label').setOutputCol('indexedLabel').fit(data)
    featureIndexer = VectorIndexer().setInputCol('features').setOutputCol('indexedFeatures').setMaxCategories(4).fit(
        data)
    # 标签列和特征列，进行索引并重命名
    labelConverter = IndexToString().setInputCol('prediction').setOutputCol('predicredLabel').setLabels(
        labelIndexer.labels)
    trainingData, testData = data.randomSplit([0.7, 0.3])
    dtClassifier = DecisionTreeClassifier().setLabelCol('indexedLabel').setFeaturesCol('indexedFeatures')
    dtPipeline = Pipeline().setStages([labelIndexer, featureIndexer, dtClassifier, labelConverter])
    dtModel = dtPipeline.fit(trainingData)
    dtPredictions = dtModel.transform(testData)
    dtPredictions.select('predicredLabel', 'label', 'features').show(10)
    evaluator = MulticlassClassificationEvaluator().setLabelCol('indexedLabel').setPredictionCol('prediction') #原始数字标签和预测标签比较
    dtAccuracy = evaluator.evaluate(dtPredictions)
    print(dtAccuracy)
    treeModelClassifier = dtModel.stages[2] #第3个索引
    print(str(treeModelClassifier.toDebugString))
