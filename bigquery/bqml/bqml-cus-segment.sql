-- create k-means model with k as 3
CREATE MODEL
  my_dataset.customer_segmentation_1
OPTIONS
  ( model_type = 'kmeans',
    num_clusters = 3,
    distance_type = 'euclidean') AS
SELECT
  Age,
  Income,
  CCAvg,
  Mortgage
FROM
  my_dataset.abcbank


-- check the evaluation of the model
SELECT
  *
FROM
  ML.EVALUATE(model my_dataset.customer_segmentation_1)


-- get the clustering result for each sample
SELECT
  *
FROM
  ML.PREDICT(model my_dataset.customer_segmentation_1,
    table my_dataset.abcbank)

SELECT
  centroid_id, ID, Age, Income, CCAvg, Mortgage
FROM
  ML.PREDICT(model my_dataset.customer_segmentation_1,
    table my_dataset.abcbank)