import twitter, dataset, time
SIX_HOURS = 21600
class TrendAnalyzer:

    def __init__(self):
        self.db = dataset.connect("sqlite:///database.db")
        self.db_discovered = dataset.connect("sqlite:///discovered.db")
        self.db_history = dataset.connect("sqlite:///history.db")

    def list_to_string(self, liste):
        return ",".join(str(element) for element in liste)

    def string_to_list(self, string):
        return string.split(",")

    def start(self):
        table_discovered = self.db_discovered["discovered"]
        table_history_occurences = self.db_history["occurences"]
        while True:
            for project in table_discovered:
                if not table_history_occurences.find_one(project_id=project["id"]):
                    table_history_occurences.insert(dict(project_id=project["id"], history_occurences=str(project['occurences'])))
                else:
                    project_row = table_history_occurences.find_one(project_id=project["id"])
                    history_occurences = self.string_to_list(project_row["history_occurences"]).append(project['occurences'])
                    data = dict(id=project_row["id"], history_occurences=self.list_to_string(history_occurences))
                    table_history_occurences.update(data, ['id'])
            time.sleep(SIX_HOURS)


trend_analyzer = TrendAnalyzer()
if __name__ == "__main__":
    trend_analyzer.start()
