
###FORENOTE
This project isn't done and can still be upgraded in my ways.

###GOAL
The idea is to track early followers of all-star projects.

1. Search the 100 first followers of every project
2. Cross-verification if they were in the first 100 followers of other projects, and if so, we increase the corresponding count
3. We organize them by number of common projects followed
4. We continuously track them, checks their recent followings.
5. Again, cross-verification with other followers of the same and different categories if followed same project
	If so, we increase count

###USE
Write the projects' twitter usernames in app/projects.txt file.
To initally get all the first 100 users of the projects, launch crawler.py.
To update the occurences, launch tracker.py.

###ISSUES
Impossible to fetch the first 100 followers of projects with more than 5k followers.



###TO DO

- manage case where there are more than 5k followers, we have to use the cursor and so on