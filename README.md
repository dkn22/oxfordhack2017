# oxfordhack2017

Our idea is to build a news engine for responsible citizenship in the post-truth world.

Every news search is scored for political bias and we attempt to verify the quotes made in each article. We recommend the news on the opposing end of the political spectrum, promoting a more balanced news diet and engagement in debate [TODO].

The political bias classifier is a Multi-size Convolutional Neural Net trained on [Congressional Records](http://www.icpsr.umich.edu/icpsrweb/ICPSR/studies/33501), with text transformed to word embeddings trained on Google News. You can also find a logistic regression model trained on the bag-of-words representation of the speeches in the models folder.

If you wish to help us drive this idea forward, please get in touch!
