import twitter, dataset, time
N_FIRST = 200
class Crawler:

    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        self.api = twitter.Api(consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token_key=token,
                        access_token_secret=token_secret,
                        sleep_on_rate_limit=True)
        self.db = dataset.connect("sqlite:///database.db")

    def list_to_string(self, liste):
        return ",".join(str(element) for element in liste)

    def string_to_list(self, string):
        return string.split(",")

    def crawl(self, force=False):
        """
        Iterate the txt file and analyze every user in it.
        force : forces crawling again, in case we increase the first_n
        """
        table = self.db["projects"]
        with open("projects.txt", "r") as fp:
            for user in fp:
                name = user.strip('\n')
                if force or not table.find_one(name=name):
                    self.update_followings(name)
                    time.sleep(1)

    def update_followings(self, screenname):
        """
        Update the followings.
        """
        #get first 100 followers
        table = self.db["followers"]
        followers = self.api.GetFollowers(screen_name=screenname)[:-N_FIRST]
        for follower in followers:
            #If not in the table, we add it
            if not table.find_one(follower_id=follower.id):
                table.insert(dict(follower_id=follower.id, name=follower.screen_name, occurences=1, featured_in=self.list_to_string([screenname])))
            #else, we update the occurences if the project name isn't already accounted for, i.e new project
            else:
                follower_row = table.find_one(follower_id=follower.id)
                if screenname not in self.string_to_list(follower_row["featured_in"]):
                    featured_in = self.string_to_list(follower_row["featured_in"])+[screenname]
                    data = dict(id=follower_row["id"], occurences=follower_row['occurences']+1, featured_in=self.list_to_string(featured_in))
                    table.update(data, ['id'])
        #insert the project name
        self.db["projects"].insert(dict(name=screenname))

crawler = Crawler("7YdRm86pJeP9p3qkkzdubdzgg","ToFJgobmck4QLWtxi4dR8nqRNZkbS7KpJ4fSMfyArsFTv09LLS",
                "828223247929974784-51g8gchXemjnn8QTehbriSget8a9xjz", "USouHNkSkPYxUL9yTLlft2qaWAGRCfQ54j95tJJgbpslx")

if __name__ == "__main__":
    crawler.crawl()
