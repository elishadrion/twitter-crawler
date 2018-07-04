import twitter, dataset
N_FIRST = 10
class Tracker:

    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        self.api = twitter.Api(consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token_key=token,
                        access_token_secret=token_secret,
                        sleep_on_rate_limit=True)
        self.db = dataset.connect("sqlite:///database.db")
        self.db_discovered = dataset.connect("sqlite:///discovered.db")


    def list_to_string(self, liste):
        return ",".join(str(element) for element in liste)

    def string_to_list(self, string):
        return string.split(",")

    def start(self):
        table_discovered = self.db_discovered["discovered"]
        table_followers = self.db['followers']
        #need to make it so we don't have to precise the max size of occurences
        #which would be the number of projects in the projects.txt
        while True:
            for i in range(9, 3, -1):
                #For all the early followers of the projects we have precised, we are going to check their latest 10 subscriptions
                #and "cross-verificate" them with the rest of the followers
                follower_rows = table_followers.find(occurences=i)
                for follower in follower_rows:
                    #get their 10 latest followings
                    try:
                        friends = self.api.GetFriends(user_id=follower['follower_id'])[:N_FIRST]
                        for friend in friends:
                            if not table_discovered.find_one(discovered_id=friend.id):
                                table_discovered.insert(dict(discovered_id=friend.id, name=friend.screen_name, occurences=1, featured_in=self.list_to_string([follower['follower_id']])))
                            else:
                                #We are measuring how frequent the user/project is subscribed by the "followers"
                                discovered_row = table_discovered.find_one(discovered_id=friend.id)
                                if str(follower['follower_id']) not in self.string_to_list(discovered_row["featured_in"]):
                                    featured_in = self.string_to_list(discovered_row["featured_in"])+[follower['follower_id']]
                                    data = dict(id=discovered_row["id"], occurences=discovered_row['occurences']+1, featured_in=self.list_to_string(featured_in))
                                    table_discovered.update(data, ['id'])
                    except:
                        print ("follower id : ", follower['follower_id'])




tracker = Tracker("7YdRm86pJeP9p3qkkzdubdzgg","ToFJgobmck4QLWtxi4dR8nqRNZkbS7KpJ4fSMfyArsFTv09LLS",
                "828223247929974784-51g8gchXemjnn8QTehbriSget8a9xjz", "USouHNkSkPYxUL9yTLlft2qaWAGRCfQ54j95tJJgbpslx")

if __name__ == "__main__":
    tracker.start()
