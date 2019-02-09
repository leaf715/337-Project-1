import json
import nltk
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
    # Strips hashtags, tags, punctuation, and RTs from text and stores text in tweets list
    # Other preprocessing such as removing stop words can go here
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
    # Get tweets that contain the word host
    host_tweets = get_relevant_tweets(["host"], tweets)
    potential_hosts = get_names(host_tweets)
    potential_hosts = sorted(potential_hosts.items(), key = lambda x: x[1], reverse=True)
    # if top two results are close, then there were cohosts
    # get better identifier than if gap was < 100 tweets
    if potential_hosts[1][1] - potential_hosts[0][1] < 100:
        print('CoHosts: '+potential_hosts[0][0]+' and '+potential_hosts[1][0])
    else:
        print('Host: '+potential_hosts[0][0])

    for award in award_names:
        print('\n')
        # everything in this section is temporary and shitty
        # We need a way to get all the ways that an award can be mentioned in a tweet
        # Also get names does not work when the award is for a movie not an actor
        keys = award.split()
        if '-' in keys:
            keys.remove('-')
        if 'Best' in keys:
            keys.remove('Best')
        # get tweets
        relevant_tweets = get_relevant_tweets(keys, tweets)
        for i in range(len(relevant_tweets)):
            tweet = relevant_tweets[i]
            tweet = tweet.replace('Best','')
            for key in keys:
                tweet = tweet.replace(key,'')

            relevant_tweets[i] = tweet
        # trim tweets for ones about the presenter and winner
        # presenter_tweets = get_relevant_tweets(['present'], relevant_tweets) This doesnt work no one uses the word presenter
        winner_tweets = get_relevant_tweets(['win'], relevant_tweets)
        people_involved = get_names(relevant_tweets)
        potential_presenters = get_names(relevant_tweets)#(presenter_tweets)
        potential_winners = get_names(winner_tweets)
        # the order here is based on me assuming the winner will be tweeted about the most
        # maybe presenter should be first idk
        potential_winners = sorted(potential_winners.items(), key = lambda x: x[1], reverse=True)
        if potential_winners:
            winner = potential_winners[0][0]
        else:
            winner = "shit broke"
        if winner in potential_hosts:
            del potential_presenters[winner]
        if winner in people_involved:
            del people_involved[winner]
        potential_presenters = sorted(potential_presenters.items(), key = lambda x: x[1], reverse=True)
        if potential_presenters:
            presenter = potential_presenters[0][0]
        else:
            presenter = "shit broke"
        if presenter in people_involved:
            del people_involved[presenter]
        people_involved = sorted(people_involved.items(), key = lambda x: x[1], reverse=True)
        if len(people_involved) >= 4:
            nominees = [people_involved[0][0], people_involved[1][0], people_involved[2][0], people_involved[3][0], winner]
        else:
            nominees = "shit broke"
        print('Award: '+award+'\nPresenter: '+presenter+'\nWinner: '+winner+'\nNominees: ')
        print(nominees)


def get_relevant_tweets(keys, tweets):
    # Get subset of tweets that contain 60%+ of the words in the keys list
    # Can adjust this required %, or weight the keys based on importance. For example, Best is
    # part of every award name, but DeMille is the most important word in that long ass award's
    # name
    relevant = []
    total_keys = len(keys)
    for tweet in tweets:
        keysfound = 0
        for key in keys:
            if re.search(key, tweet, re.IGNORECASE):
                keysfound+=1
        if float(keysfound)/float(total_keys) >= 0.6:
            relevant.append(tweet)

    return relevant

def get_names(tweets):
    # Find names based on first letter being capital of two consecutive words
    #  and then counting the number of times they show up
    # Definitely better way of identifying names but this is simple
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
