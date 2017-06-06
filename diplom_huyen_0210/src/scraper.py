from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
text = " ".join(df_tweets['text'].values.astype(str))
no_urls_no_tags = " ".join([word for word in text.split()
                                if 'http' not in word
                                    and not word.startswith('@')
                                    and word != 'RT'
                                ])
# mask = np.array(imread("twitter_mask.png", flatten=True))
# mask = np.array(Image.open("twitter_mask1.png"))

wc = WordCloud(font_path='/Fonts/CabinSketch-Bold.ttf', background_color="white", stopwords=STOPWORDS,max_words=500,width=1800,
    height=1400, mask=mask)
wc.generate(no_urls_no_tags)
plt.imshow(wc)
plt.axis("off")
# show
plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.figure()
# plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
# plt.axis("off")
plt.show()