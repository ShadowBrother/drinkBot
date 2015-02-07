#fix for url_for, prepends "/flask" to routes
import flask

def url_for(endpoint, **kwargs):
	return "/flask" + flask.url_for(endpoint, **kwargs)

#for use as jinja2 template filter
def routeFix(route):
	return "/flask" + route
