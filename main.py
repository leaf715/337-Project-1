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
    all_keys = {}
    for award in award_names:
        keys = award.split(' ')
        for key in keys:
            if key == 'Award':
                break
            if key in all_keys.keys():
                all_keys[key] += 1
            else:
                all_keys[key] = 1
    unique_keys = {k:v for k,v in all_keys.items() if v <= 1}
    unique_keys = list(unique_keys.keys())
    unique_keys.append('Supporting')
    unique_keys.remove('Language')
    (unique_keys)
    tweets = strip_raw_tweets(raw_tweets, tweets)

    master(tweets,award_names)
    winner_tweets = get_relevant_tweets(['win'], tweets)

    print "RealStuff"
    get_red_carpet(tweets)

    #get_nominees_movies(winner_tweets,award_names)
    get_winner_movies(winner_tweets,award_names)


    #hosts = get_hosts(tweets)

    get_winner_ppl(winner_tweets,award_names)

    #get_presenters(tweets, award_names, unique_keys)

def master(tweets, awards):
    for award in awards:
        print i

def get_presenters(tweets, award_names, unique_keys):
    p_tweets = []
    present_keys = ['present', 'will present', 'is presenting', 'are presenting', 'will be present']
    for tweet in tweets:
        for key in present_keys:
            key = '[A-Z][a-z]* [A-Z][a-z]* '+key
            if re.search(key,tweet, re.IGNORECASE):
                p_tweets.append(tweet)
        if re.search('presented by [A-Z][a-z]* [A-Z][a-z]*', tweet, re.IGNORECASE):
            p_tweets.append(tweet)

    # m,f = get_people(p_tweets)
    # p = m.union(f) - winners - hosts
    for award in award_names:
        print(' ')
        relevant = p_tweets
        keys = award.split(' ')

        bad_keys = set()
        if '-' in keys:
            keys.remove('-')
            awardnodash = ' '.join(keys)
            leftright = award.split('-')
            keys = keys + leftright

        if 'or' in keys:
            keys.remove('or')
        # keys = keys + [keys[i] + ' ' + keys[i+1] for i in range(len(keys)-1)]
        keys.append(awardnodash)
        if 'Best' in keys:
            keys.remove('Best')
        if 'Actor' in keys:
            relevant = get_relevant_tweets(['Actor'], relevant)
            if 'Supporting' not in keys:
                relevant = remove_wrong_section(['Supporting Actor'],relevant)
        elif 'Actress' in keys:
            relevant = get_relevant_tweets(['Actress'], relevant)
            if 'Supporting' not in keys:
                relevant = remove_wrong_section(['Supporting Actress'],relevant)
        else:
            relevant = remove_wrong_section(['Actor', 'Actress'], relevant)
        if 'Television' in keys:
            keys.append('TV')
            relevant = remove_wrong_section(['Picture'], relevant)
        else:
            relevant = remove_wrong_section(['TV', 'Television'], relevant)
        total_keys = len(keys)
        print(keys)
        for key in keys:
            if key in unique_keys:
                relevant = get_relevant_tweets([key], relevant)
        match_dict = {}
        for tweet in relevant:
            keysfound = 0
            for key in keys:
                if re.search(key,tweet, re.IGNORECASE):
                    keysfound += 1
            match_dict[tweet] = float(keysfound)/float(total_keys)
        sorted_dict = sorted(match_dict.items(), key = lambda x: x[1], reverse=True)
        top_tweets = []
        for i in range(int(len(sorted_dict)/2)):
            k = sorted_dict[i][0]
            top_tweets.append(k)
        # presenters = get_winner(p,top_tweets)
        print(award)
        i = 0
        keys = keys + award.split(' ')
        while i < len(sorted_dict):
            tweet = sorted_dict[i][0]
            words = tweet.split(' ')
            presenters = set()
            j = 0
            while j < len(words)-1:
                if words[j].istitle() and words[j] != 'I':
                    if words[j+1].istitle() and words[j+1] != 'I':
                        presenters.add(words[j]+' '+words[j+1])
                        j += 1
                j += 1
            goodpresenters = copy.deepcopy(presenters)
            for potential_p in presenters:
                for key in keys:
                    if re.search(key, potential_p, re.IGNORECASE):
                        goodpresenters.discard(potential_p)
            if len(goodpresenters) > 0:
                print(goodpresenters)
                break
            i += 1

def strip_raw_tweets(raw_tweets,tweets):
        # Strips hashtags, tags, punctuation, and RTs from text and stores text in tweets list
        # Other preprocessing such as removing stop words can go here
        for tweet in raw_tweets:
            text = tweet["text"].split()
            stripped_text = " ".join(word for word in text if word[0] is not '#' and word[0] is not '@')
            stripped_text = stripped_text.replace('\'s','')
            stripped_text = stripped_text.replace('.','')
            stripped_text = stripped_text.replace(',','')
            stripped_text = stripped_text.replace('Golden Globes','')
            stripped_text = stripped_text.replace('@','')
            stripped_text = stripped_text.replace('#','')
            if stripped_text.find('RT') != -1:
                stripped_text = stripped_text[:stripped_text.find('RT')]
            tweets.append(stripped_text)
        return tweets

def get_red_carpet(tweets):
    rcTweets =  get_relevant_tweets(['red carpet'], tweets)
    #for i in rcTweets:
        #print i
    mostMentionedM,mostMentionedF = get_people_rc(rcTweets)
    print get_winner_m2(mostMentionedF)
    print get_winner_m2(mostMentionedM)

    bestTweets = get_relevant_tweets(['best dressed'], tweets)

# Get actor and actress names
def get_people_rc(tweets):
    men = dict()
    women = dict()
    bad = ['Red','Carpet','Dress']
    for tweet in tweets:
        poss_name = re.search("[A-Z][a-z]* [A-Z][a-z]*", tweet)
        if poss_name:
            name = poss_name.group(0)
            first = name.split(' ',1)[0]
            last =  name.split(' ',1)[1]
            if first not in bad and last not in bad:
                if name in women or first in names.words('female.txt'):
                    women[name] = women.get(name, 0) + 1
                elif name in men or first in names.words('male.txt'):
                    men[name] = men.get(name, 0) + 1

    return men, women

def get_hosts(tweets):
    # Get tweets that contain the word host
    host_tweets = get_relevant_tweets(["host"], tweets)
    potential_hosts = get_names(host_tweets)
    potential_hosts = sorted(potential_hosts.items(), key = lambda x: x[1], reverse=True)
    # if top two results are close, then there were cohosts
    # get better identifier than if gap was < 100 tweets
    if potential_hosts[1][1] - potential_hosts[0][1] < 100:
        print('CoHosts: '+potential_hosts[0][0]+' and '+potential_hosts[1][0])
        return set([potential_hosts[0][0], potential_hosts[1][0]])
    else:
        print('Host: '+potential_hosts[0][0])
        return set([potential_hosts[0][0]])

def get_winner_ppl(tweets,award_names):
    previous_winners_ppl = set()
    # match actors and actresses to awards
    for award in award_names:
        # preprocess keys given to tweet searcher
        leftright = award.split('-')
        keys = leftright[0].split()
        bad_keys = set()
        if len(leftright) > 1:
            category = leftright[1].split()
            if 'or' in category:
                category.remove('or')
            if 'Motion' in category:
                category.remove('Motion')
            if 'Picture' in category:
                category.append('Film')
                bad_keys.add('TV')
                bad_keys.add('Television')
            if 'Television' in category:
                category.append('TV')
                bad_keys.add('Picture')
            if 'Drama' in category:
                bad_keys.add('Comedy')
                bad_keys.add('Musical')
            if 'Comedy' in category:
                bad_keys.add('Drama')
            if 'Miniseries' in category:
                bad_keys.add('Drama')
                bad_keys.add('Comedy')
                bad_keys.add('Musical')
            else:
                bad_keys.add('series')
        else:
            category = []

        if 'Best' in keys:
            keys.remove('Best')
        if 'Motion' in keys:
            keys.remove('Motion')
        if 'Picture' in keys:
            keys.append('Film')
            bad_keys.add('TV')
            bad_keys.add('Television')
        if 'Television' in keys:
            keys.append('TV')
            bad_keys.add('Picture')
        # Get relevant tweets
        relevant_tweets_keys = get_relevant_tweets(keys, tweets)
        relevant_tweets_uncleaned = get_relevant_tweets(category, relevant_tweets_keys)
        relevant_tweets = remove_wrong_section(bad_keys, relevant_tweets_uncleaned)
        winner_tweets = get_relevant_tweets(['win','congrats'], relevant_tweets)
        winners_m, winners_f = get_people_rc(winner_tweets)
        if 'Actor' in keys:
            winner_set = winners_m #- previous_winners_ppl
        elif 'Actress' in keys:
            winner_set = winners_f #- previous_winners_ppl
        else:
            continue
        winner = get_winner_m(winner_set)
        print(award)
        print(winner)
        # 4 people in history have won 2 individual awards in the same year I'll take that bet
        previous_winners_ppl.add(winner)
    return previous_winners_ppl

def get_winner_movies(tweets,award_names):
    previous_winners_ppl = set()
    # match movies to awards
    for award in award_names:
        if 'Actor' not in award and 'Actress' not in award and 'Achievement' not in award and 'Director' not in award:
            # preprocess keys given to tweet searcher
            leftright = award.split('-')
            keys = leftright[0].split()
            bad_keys = set()
            bad_keys.add('Actor')
            bad_keys.add('Actress')
            bad_keys.add('Director')
            if len(leftright) > 1:
                category = leftright[1].split()
                if 'or' in category:
                    category.remove('or')
                if 'Motion' in category:
                    category.remove('Motion')
                if 'Picture' in category:
                    category.append('Film')
                    bad_keys.add('TV')
                    bad_keys.add('Television')
                if 'Television' in category:
                    category.append('TV')
                    bad_keys.add('Picture')
                if 'Drama' in category:
                    bad_keys.add('Comedy')
                    bad_keys.add('Musical')
                if 'Comedy' in category:
                    bad_keys.add('Drama')
                if 'Miniseries' in category or 'Miniseries' in keys:
                    bad_keys.add('Drama')
                    bad_keys.add('Comedy')
                    bad_keys.add('Musical')
                if 'Score' in category or 'Score' in keys:
                    bad_keys.add('Song')
                if 'Song' in category or 'Song' in keys:
                    bad_keys.add('Score')
                else:
                    bad_keys.add('series')
            else:
                category = []

            if 'Best' in keys:
                keys.remove('Best')
            if 'Motion' in keys:
                keys.remove('Motion')
            if 'Picture' in keys:
                keys.append('Film')
                bad_keys.add('TV')
                bad_keys.add('Television')
            if 'Television' in keys:
                keys.append('TV')
                bad_keys.add('Picture')
            if 'Miniseries' in keys:
                keys.append('series')

            # Get relevant tweets
            relevant_tweets_keys = get_relevant_tweets(keys, tweets)
            relevant_tweets_uncleaned = get_relevant_tweets(category, relevant_tweets_keys)
            relevant_tweets = remove_wrong_section(bad_keys, relevant_tweets_uncleaned)
            winner_tweets = get_relevant_tweets(['congrat', 'win'], relevant_tweets)
            mentioned = get_movie_names2(winner_tweets)
            winner = get_winner_m(mentioned)
            mention = cleanDict(mentioned,3)
            print(award)
            print(winner)
            #for tweet in winner_tweets:
            #    print(tweet)

    return previous_winners_ppl

def get_winner_m(mentioned):
    maxv = 0
    winningKey = ""
    for key in mentioned:
        v = mentioned[key]
        if v > maxv:
            maxv = v
            winningKey = key
    return winningKey

def get_winner_m2(mentioned):
    nomKeys = set()
    for x in range(5):
        maxv = 0
        winningKey = ""
        for key in mentioned:
            v = mentioned[key]
            if v > maxv:
                maxv = v
                winningKey = key
        mentioned[winningKey] = 0
        nomKeys.add(winningKey)
    return nomKeys

# Find winner most associated with award
def get_winner(possible, tweets):
    match_dict = dict((name, 0) for name in list(possible))
    allwords = ' '.join(tweets)
    for p in possible:
        # without the space at the end people who spell like shit mess everything up
        match_dict[p] = allwords.count(p+' ')
    sorted_dict = sorted(match_dict.items(), key = lambda x: x[1], reverse=True)
    winner = sorted_dict[0][0]
    return winner

# get tweets that contain any of the keys
def get_relevant_tweets(keys, tweets):
    relevant = []
    for tweet in tweets:
        for key in keys:
            if re.search(key, tweet, re.IGNORECASE):
                relevant.append(tweet)
                break

    return relevant

# Gets rid of tweets about wrong award because some of them have very similar keys
def remove_wrong_section(bad_keys, tweets):
    relevant = []
    for tweet in tweets:
        for key in bad_keys:
            if not any(key in tweet for key in bad_keys):
                relevant.append(tweet)
    return relevant

# Get actor and actress names
def get_people(tweets):
    men = dict()
    women = dict()
    for tweet in tweets:
        words = [nltk.word_tokenize(tweet)]
        tagged_words = [nltk.pos_tag(word) for word in words][0]
        for chunk in nltk.ne_chunk(tagged_words):
            if type(chunk) == nltk.tree.Tree:
                # Adele needs a last name but other than her its fine to look for first and last
                if chunk.label() == 'PERSON' and len(chunk) > 1 and len(chunk) < 3:
                    name = (' '.join([c[0] for c in chunk]))
                    first = name.split(' ',1)[0]
                    if first in names.words('male.txt'):
                        men[name] = men.get(name, 0) + 1
                    if first in names.words('female.txt'):
                        women[name] = women.get(name, 0) + 1

    return men, women

def get_people2(tweets):
    men = dict()
    women = dict()
    possible_movies_dict = dict()

    for tweet in tweets:
        result = re.search('Congratulations(.*)win', tweet)
        result2 = re.search('winner is(.*)for', tweet)
        result3 = re.search('Congrats(.*)win', tweet)
        result4 = re.search('(.*)wins', tweet)
        oneIsTrue = False
        if result:
            movName = result.group(1)
            oneIsTrue = True
        if result2:
            movName = result2.group(1)
            oneIsTrue = True
        if result3:
            movName = result3.group(1)
            oneIsTrue = True
        if result4:
            movName = result4.group(1)
            oneIsTrue = True
        if oneIsTrue and len(movName.split()) <3 and len(movName.split()) >1:
            movName = movName.replace('to ','')
            movName = movName.replace('for ','')
            movName = movName.replace('on ','')
            movName = movName.replace("'","'")
            name = movName.split()
            if name[0]:
                if name[0] in names.words('male.txt'):
                    men[movName] = men.get(movName, 0) + 1
                if name[0] in names.words('female.txt'):
                    women[movName] = women.get(movName, 0) + 1

    return men, women
#gets possible movie names from tweets/not used anymore
def get_movie_names(tweets):
    possible_movies_dict = dict()
    possible_movies = set()
    badd = ["Original Song","Motion Picture","Golden Globes"]
    for tweet in tweets:
        words = tweet.split()
        #first word always capitalized
        words.pop(0)
        currentlyCap = False
        wordsInTitle = 0
        poss_title =""
        for word in words:
            if(currentlyCap):
                if(word[0].isupper()):
                    poss_title += " " + word
                    wordsInTitle += 1
                else:
                    currentlyCap = False
                    if "Best" not in poss_title:
                        if(wordsInTitle > 3):
                            possible_movies_dict[poss_title] = possible_movies_dict.get(poss_title, 0) + 1
                            possible_movies.add(poss_title)
                        if(wordsInTitle == 1 and isNotCommonWord(poss_title)):
                            possible_movies_dict[poss_title] = possible_movies_dict.get(poss_title, 0) + 1
                            possible_movies.add(poss_title)
                        if(wordsInTitle == 2 and poss_title not in badd):
                            possible_movies_dict[poss_title] = possible_movies_dict.get(poss_title, 0) + 1
                            possible_movies.add(poss_title)
                        if(wordsInTitle == 3 and poss_title != "Best Original Song"):
                            possible_movies_dict[poss_title] = possible_movies_dict.get(poss_title, 0) + 1
                            possible_movies.add(poss_title)
                    poss_title = ""
                    wordsInTitle = 0
            else:
                if(word[0].isupper()):
                    currentlyCap = True
                    poss_title = word
                    wordsInTitle = 1
    return possible_movies_dict
#GetWinnerMovieName
def get_movie_names2(tweets):
    possible_movies_dict = dict()
    print len(tweets)
    for tweet in tweets:
        result = re.search('Congratulations(.*)win', tweet)
        result2 = re.search('winner is(.*)for', tweet)
        result3 = re.search('Congrats(.*)win', tweet)
        result4 = re.search('(.*)wins', tweet)
        oneIsTrue = False
        if result:
            movName = result.group(1)
            oneIsTrue = True
        if result2:
            movName = result2.group(1)
            oneIsTrue = True
        if result3:
            movName = result3.group(1)
            oneIsTrue = True
        if result4:
            movName = result4.group(1)
            oneIsTrue = True
        if oneIsTrue and len(movName.split()) <6:
            movName = movName.replace('to ','')
            movName = movName.replace('for ','')
            movName = movName.replace('on ','')
            movName = movName.replace("'","'")
            possible_movies_dict[movName] = possible_movies_dict.get(movName, 0) + 1
    return possible_movies_dict

def isNotCommonWord(word):
    more_stop = ['win','best','film','tv','musical','comedy','drama','animated','picture','motion','series','golden','globes']
    if word.lower() in stop or word.lower() in more_stop:
        return False
    else:
        return True

def cleanDict(comp, num):
    new = dict()
    for i in comp:
        if comp[i] > num:
            new[i] = comp[i]
    return new


# Old function that still works for host so I left it in
def get_names(tweets):
    ppl_and_movies = {}
    for tweet in tweets:
        words = [nltk.word_tokenize(tweet)]
        tagged_words = [nltk.pos_tag(word) for word in words][0]
        for chunk in nltk.ne_chunk(tagged_words):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON' and len(chunk) > 1:
                    name = (' '.join([c[0] for c in chunk]))
                    if name in ppl_and_movies.keys():
                        ppl_and_movies[name] = ppl_and_movies[name] + 1
                    else:
                        ppl_and_movies[name] = 1

    return ppl_and_movies

if __name__ == "__main__":
    main()
