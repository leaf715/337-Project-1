import json

def main():
    print("running")
    cfg_file = open("award_show.config", "r")
    cfg_lines = cfg_file.readlines()
    data_path = json.loads(cfg_lines[0])
    award_names = json.loads(cfg_lines[1])
    raw_data = open(data_path, "r")
    raw_tweets = json.loads(raw_data.read())
    tweets = []
    for tweet in raw_tweets:
        tweets.append(tweet["text"])
    print(tweets[0])

if __name__ == "__main__":
    main()
