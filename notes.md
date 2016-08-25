# Notes on Class 8 and Class 9

## Class 8

### Intro Text

Something like this:

> You have started to learn about databases, but you haven't yet seen how to incorporate them into an app. So today, we'll simply add a few features onto our project, and get everything teed up for next class, when we will finally start persisting user data in a database.

> Today we will expand our project so that users can actually view their list of movies. We will also introduce a second list view, representing the movies that the user has watched (crossed off). In this second view, users will be able to give each movie a rating between 1 and 5 stars.

### Before Walkthrough 8

These changes will already be in place. Briefly explain them:

- 400 error 
	- We don't bother giving a nice error message to a malicious user 
- change "cross off" semantics to "watched it" semanics. Instead of "crossing off a movie from your list", user is reporting that she "finished watching" that movie
	- rename `CrossOffMovie` handler to `WatchedMovie`, change route to `"/watched-it"`
	- change a bunch of variable names in `WatchedMovie.post` method and the `edit.html` template
	- change the confirmation template to `watched-it-confirmation.html`
	- change name of `getCurrentWatchlist()` function to `getUnwatwchedMovies()`


### During Walkthrough 8

- implement "List View" on the home page
	- in `edit.html` template, make a `ul` and show the unwatched movies under a header like `<h2>Movies I Want to Watch:</h2>`
	- rename `edit.html` to the more generic name of `frontpage.html`

- change the "watched-it" form. Instead of a dropdown at the bottom of the page, use a button on each list view item
	- delete code for the second form in `frontpage.html`
	- in the list view, each `li` should have its own little form
		- `action` goes to `/watched-it`
		- submit button says `"I Watched it!"
		- add a hidden input to pass the particular movie as a param

- implement second list view of "Movies I have Watched"
	- create a similar function `getWatchedMovies()` which returns a different list of movie titles (hard-coded fake stuff)
	- add a `/ratings` route to the app handled by a new handler class called `MovieRatings`, with a `get` method stub like `self.response.write("testing 1 2 3...")`
	- implement `MovieRatings.get`. It should render a template `ratings.html` which for now just lists the movies from `getWatchedMovies` under a header `<h2>Movies I Have Watched</h2>`
	- add a nav menu in `scaffolding.html` so users can actually navigate between the two list views (front page and ratings page). Make the big `<h1>` not a link anymore.


### During Studio 8

Implement the feature where users can rate the movies the have watched

1. Make a confirmation template 
2. Handle form submission so that it renders the template 
3. Add the forms, one on each list item in the `ratings.html` template

