import json
import nltk
from nltk.corpus import stopwords, names
stop = stopwords.words('english')
# http://www.nltk.org/
import re
# https://docs.python.org/3/library/re.html

def main():
    cfg_file = open("award_show.config", "r")
    cfg_lines = cfg_file.readlines()
    data_path = json.loads(cfg_lines[0])
    award_names = json.loads(cfg_lines[1])
    raw_data = open(data_path, "r")
    raw_tweets = json.loads(raw_data.read())
    tweets = []
    for tweet in raw_tweets:
        text = tweet["text"].split()
        stripped_text = " ".join(word for word in text if word[0] is not '#' and word[0] is not '@')
        stripped_text = stripped_text.replace('\'s','')
        stripped_text = stripped_text.replace('.','')
        stripped_text = stripped_text.replace(',','')
        stripped_text = stripped_text.replace('Golden Globes','')
        if stripped_text.find('RT') != -1:
            stripped_text = stripped_text[:stripped_text.find('RT')]
        tweets.append(stripped_text)
    host_tweets = get_relevant_tweets(["host"], tweets)
    potential_hosts = get_names(host_tweets)
    potential_hosts = sorted(potential_hosts.items(), key = lambda x: x[1], reverse=True)
    if potential_hosts[1][1] - potential_hosts[0][1] < 100:
        print('CoHosts: '+potential_hosts[0][0]+' and '+potential_hosts[1][0])
    else:
        print('Host: '+potential_hosts[0][0])

def get_relevant_tweets(keys, tweets):
    relevant = []
    for tweet in tweets:
        for key in keys:
            if re.search(key, tweet, re.IGNORECASE):
                relevant.append(tweet)
                break
    return relevant

def get_names(tweets):
    names = {}
    for tweet in tweets:
        words = tweet.split()
        for i in range(len(words)):
            if words[i][0].isupper():
                if i + 1 < len(words) - 1:
                    if words[i+1][0].isupper():
                        name = (words[i] + ' ' + words[i+1])
                        if name in names.keys():
                            names[name] = names[name] + 1
                        else:
                            names[name] = 1

    return names

if __name__ == "__main__":
    main()
