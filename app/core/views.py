from flask import redirect, url_for, render_template, request
import dataset

from ..core import core


@core.route('/')
def index():
	return render_template("index.html")

@core.route('/discovered')
def discovered():
	db_discovered = dataset.connect("sqlite:///app/discovered.db")
	results = db_discovered.query("SELECT * FROM discovered ORDER BY occurences DESC, id DESC")
	return render_template("display.html", results=results)

@core.route('/followers/<int:occurences>')
def followers(occurences):
	db_followers = dataset.connect("sqlite:///app/database.db")
	results = db_followers['followers'].find(occurences=int(occurences))
	return render_template("display_followers.html", results=results)

@core.route('/discovered/<int:rank>')
def discovered_rank(rank):
    db_followers = dataset.connect("sqlite:///app/database.db")
    db_discovered = dataset.connect("sqlite:///app/discovered.db")

    #We get the early followers with the corresponding rank
    early_followers = set()
    follower_rows = db_followers['followers'].find(occurences=rank)
    for row in follower_rows:
        early_followers.add(row['follower_id'])

    #we get the projects followed by the early followers
    results = []
    for row in db_discovered['discovered'].find(order_by="-id"):
        occurences = 0
        #Tracks if the project is followed by at least one early follower
        flag = False
        #if the early follower's id is in the list, we add the project
        for element in row['featured_in'].split(","):
            if int(element) in early_followers:
                occurences += 1
                flag = True
        if flag:
            row['occurences'] = occurences
            results.append(row)

    return render_template("display.html", results=results)
