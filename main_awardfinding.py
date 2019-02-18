import json
import nltk
import copy
# nltk.download("stopwords") #getting Certificate error with this in
# nltk.download("punkt")
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('names')
# nltk.download("stopwords") #getting Certificate error with this in
from nltk.corpus import stopwords, names
stop = stopwords.words('english')
# http://www.nltk.org/
import re
# https://docs.python.org/3/library/re.html

def main():
    # Config file contains data file path and awards of that show
    cfg_file = open("award_show.config", "r")
    cfg_lines = cfg_file.readlines()
    data_path = json.loads(cfg_lines[0])
    award_names = json.loads(cfg_lines[1])
    raw_data = open(data_path, "r")
    raw_tweets = json.loads(raw_data.read())
    tweets = []
    tweets = strip_raw_tweets(raw_tweets, tweets)
    print(len(tweets))
    nlp_awards = get_award_names(tweets)
    print(nlp_awards[0:27])

def get_award_names(tweets):
    award_dict = {}
    for tweet in tweets:
        tweet = tweet.replace('!','')
        tweet = tweet.replace('.','')
        tweet = tweet.replace(':','')
        words = tweet.split(' ')
        if 'Best' in words:
            i = words.index('Best')
            award = []
            other_words = ['-', 'for', 'in', 'a']
            while i < len(words):
                if words[i] == 'At':
                    break
                if words[i].istitle():
                    award.append(words[i])
                elif words[i] in other_words:
                    if i+1 < len(words):
                        if words[i+1].istitle():
                            award.append(words[i]+' '+words[i+1])
                            i += 1
                        else:
                            break
                else:
                    break
                i += 1
            if len(award) > 1 and len(award) < 7:
                award = ' '.join(award)
                award_dict[award] = award_dict.get(award, 0) + 1
    # keys = list(award_dict.keys())
    # keys = [words.split(' ') for words in keys]
    # for i in range(len(keys)):
    #     for j in range(len(keys)):
    #         if i == j:
    #             pass
    award_dict = sorted(award_dict.items(), key = lambda x: x[1], reverse=True)
    return award_dict



def strip_raw_tweets(raw_tweets,tweets):
        # Strips hashtags, tags, punctuation, and RTs from text and stores text in tweets list
        # Other preprocessing such as removing stop words can go here
        for tweet in raw_tweets:
            text = tweet["text"].split()
            stripped_text = " ".join(word for word in text if word[0] is not '#' and word[0] is not '@')
            stripped_text = stripped_text.replace('\'s','')
            stripped_text = stripped_text.replace('.','')
            stripped_text = stripped_text.replace(',','')
            stripped_text = stripped_text.replace('Golden','')
            stripped_text = stripped_text.replace('Globes','')
            stripped_text = stripped_text.replace('@','')
            stripped_text = stripped_text.replace('#','')
            if stripped_text.find('RT') != -1:
                stripped_text = stripped_text[:stripped_text.find('RT')]
            tweets.append(stripped_text)
        return tweets

if __name__ == "__main__":
    main()
