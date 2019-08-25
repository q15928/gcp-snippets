library(data.table)
library(factoextra)

setwd("~/mds/git-repos/gcp-snippets/bigquery/bqml/")
ABC <-fread("./dataset/ABCBank.csv")# ,header=TRUE, sep=",")

ABC_feat <- scale(ABC[,2:5])
cus_seg <- kmeans(ABC_feat, centers=3, nstart=25)

fviz_cluster(cus_seg, data=ABC_feat,
             ellipse.type="convex",
             axes =c(1,2),
             geom="point",
             label="none",
             ggtheme=theme_classic())
