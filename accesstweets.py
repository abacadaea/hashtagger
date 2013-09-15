import twitter

user = raw_input("Enter user.")
subject = raw_input("Enter subject.")

api = twitter.Api()
statuses = api.GetUserTimeline(user)

for i in statuses:
	print i.text

tweets = api.GetSearch(subject, per_page=100, page=1)
