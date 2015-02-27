library(plyr)
library(ggplot2)
words <- read.delim("data/part-00000", sep="\t", quote="") # quote="" to prevent EOF errors.
colnames(words) <- c("word", "count")
words$count<- as.numeric(words$count)
sorted.words <- words[(with(words, order(count, decreasing=T))),] # This just makes it easier to look at
word.counts <- count(words$count)

#plot.word.freq.dist <- ggplot(word.counts, aes(x=freq)) + geom_histogram() + scale_x_log10()
plot.word.dist <- ggplot(words, aes(x=abs(count))) + geom_histogram() + scale_x_log10() + scale_y_log10() +
  labs(title="Word Frequency in Tweets", x="Num Times a Word Appears", y="Count")

#plot.word.freq.dist
plot.word.dist

