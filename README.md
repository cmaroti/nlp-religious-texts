# Comparing Religious Texts with NLP

For this project, I scraped the following religious texts from the [Internet Sacred Text Archive](http://www.sacred-texts.com/):
* Old Testament
* New Testament
* Quran
* Book of Mormon
* Rig Veda
* Bhagavad Gita
* Dhammapada
* Tao Te Ching
* Guru Granth Sahib
* Analects of Confucius

I trained a Word2Vec model on the corpus, and summed the vector of each word in each chapter to create chapter vectors. I then created a matrix consisting of the cosine similarity of each chapter to every other chapter.

I also calculated the sentiment score of each sentence in each chapter with TextBlob, and created a vector containing the percentages of positive, neutral, and negative sentences in the chapter. I created another matrix, but this time consisting of the cosine similarity of each chapter's sentiment vector to every other chapter's sentiment vector.

To get a final similarity matrix, I took 70% of the Word2Vec matrix and 30% of the sentiment matrix.

Finally, I built a tool that returns the most similar chapter of one text to a user-inputted chapter of another text.
