[![Build Status](https://travis-ci.org/andela/ah-scorpion.svg?branch=develop)](https://travis-ci.org/andela/ah-scorpion)
[![Coverage Status](https://coveralls.io/repos/github/andela/ah-scorpion/badge.svg?branch=develop)](https://coveralls.io/github/andela/ah-scorpion?branch=develop)<br>
Authors Haven - A Social platform for the creative at heart.
=======

## Vision
Create a community of like minded authors to foster inspiration and innovation
by leveraging the modern web.

---
## Mockup links

- [landing page](https://6zflbtxzbitjxze0azbs0w-on.drv.tw/SIMS/ah-scorpion-templates/)
- [dashboard page](https://6zflbtxzbitjxze0azbs0w-on.drv.tw/SIMS/ah-scorpion-templates/dashboard.html)
- [signup page](https://6zflbtxzbitjxze0azbs0w-on.drv.tw/SIMS/ah-scorpion-templates/signup.html)
- [login page](https://6zflbtxzbitjxze0azbs0w-on.drv.tw/SIMS/ah-scorpion-templates/login.html)
- [profile page](https://6zflbtxzbitjxze0azbs0w-on.drv.tw/SIMS/ah-scorpion-templates/profile.html)
- [view-one-article page](https://6zflbtxzbitjxze0azbs0w-on.drv.tw/SIMS/ah-scorpion-templates/view-article.html)

## API Spec
The preferred JSON object to be returned by the API should be structured as follows:

### Users (for authentication) Response

```source-json
{
  "user": {
    "email": "jake@jake.jake",
    "token": "jwt.token.here",
    "username": "jake",
    "bio": "I work at statefarm",
    "image": null
  }
}
```
### Profile Response
```source-json
{
  "profile": {
    "username": "jake",
    "bio": "I work at statefarm",
    "image": "image-link",
    "following": false
  }
}
```
### Single Article Response
```source-json
{
  "article": {
    "id": 1,
    "title": "How to train your dragon",
    "likes": 3,
    "dislikes": 1,
    "slug": "how-to-train-your-dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    },
    "averageRating": null,
    "ratingsCount": 0,
  }
}
```
### Multiple Articles Response
```source-json
{
  "articles":[{
    "id": 1,
    "title": "How to train your dragon",
    "likes": 2,
    "dislikes": 3,
    "slug": "how-to-train-your-dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    },
    "averageRating": null,
    "ratingsCount": 0,
  }, {
    "id": 2,
    "title": "How to train your dragon 2",
    "likes": 1,
    "dislikes": 0,
    "slug": "how-to-train-your-dragon-2",
    "description": "So toothless",
    "body": "It a dragon",
    "tagList": ["dragons", "training"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    },
    "averageRating": 3.5,
    "ratingsCount": 400,
  }],
  "articlesCount": 2
}
```
### Single Comment Response
```source-json
{
  "comment": {
    "id": 1,
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:22:56.637Z",
    "body": "It takes a Jacobian",
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```
### Multiple Comments Response
```source-json
{
  "comments": [{
    "id": 1,
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:22:56.637Z",
    "body": "It takes a Jacobian",
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }],
  "commentsCount": 1
}
```

### List of Ratings Response
```source-json
{
  "ratings": [
    {
      "user": "jake",
      "stars": 5
    },
    {
      "user": "jamie",
      "stars": 3
    }
  ]
}
```


### List of Tags Response
```source-json
{
  "tags": [
    "reactjs",
    "angularjs"
  ]
}
```
### Errors and Status Codes Response
If a request fails any validations, expect errors in the following format:

```source-json
{
  "errors":{
    "body": [
      "can't be empty"
    ]
  }
}
```
### Other status codes:
401 for Unauthorized requests, when a request requires authentication but it isn't provided

403 for Forbidden requests, when a request may be valid but the user doesn't have permissions to perform the action

404 for Not found requests, when a resource can't be found to fulfill the request


Endpoints:
----------

### Log In:

`POST /api/v1/users/login`

Example request body:

```source-json
{
  "email": "jake@jake.jake",
  "password": "jakejake"
}
```

No authentication required, returns a User

Required fields: `email`, `password`

### Registration:

`POST /api/v1/users/signup`

Example request body:

```source-json
{
  "username": "Jacob",
  "email": "jake@jake.jake",
  "password": "jakejake"
}
```

### Signup/Login via social Accounts( Facebook/Google):

`POST /api/v1/users/social_auth/`

Example request body:

```source-json
{
  "access_token": "<your access_token>",
  "provider": "<facebook/google-oauth2>"
}
```

No authentication required, returns a User

Required fields: `access_token` and  `provider`

### Get Current User

`GET /api/v1/user`

Authentication required, returns a User that's the current user

### Update User

`PUT /api/v1/user`

Example request body:

```source-json
{
  "email": "jake@jake.jake",
  "bio": "I like to skateboard",
  "image": "https://i.stack.imgur.com/xHWG8.jpg"
}
```

Authentication required, returns the User

Accepted fields: `email`, `username`, `password`, `image`, `bio`

### Get Profile

`GET /api/v1/profiles/:username`

Authentication optional, returns a Profile

### Follow user

`PUT /api/v1/profiles/:username/follow`

Authentication required, returns a Profile

No additional parameters required

### Unfollow user

`DELETE /api/v1/profiles/:username/follow`

Authentication required, returns a Profile

No additional parameters required

### User To Get Their Followers

`GET /api/v1/profiles/followers/`

Authentication required, returns Profiles of users who are following you

No additional parameters required

### User To Get Who They Are Following

`GET /api/v1/profiles/following/`

Authentication required, returns Profiles of users you are following

No additional parameters required

### List Articles

`GET /api/v1/articles`

Returns most recent articles globally by default, provide `tag`, `author` or `favorited` query parameter to filter results

Query Parameters:

Filter by tag:

`?tag=AngularJS`

Filter by author:

`?author=jake`

Favorited by user:

`?favorited=jake`

Limit number of articles (default is 20):

`?limit=20`

Offset/skip number of articles (default is 0):

`?offset=0`

Authentication optional, will return multiple articles, ordered by most recent first

### Feed Articles [Not Yet Implemented]

`GET /api/v1/articles/feed`

Can also take `limit` and `offset` query parameters like List Articles

Authentication required, will return multiple articles created by followed users, ordered by most recent first.

### Get Article

`GET /api/v1/articles/:slug`

No authentication required, will return single article

### Create Article

`POST /api/v1/articles`

Example request body:

```source-json
{
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "You have to believe",
    "tagList": ["reactjs", "angularjs", "dragons"],
    "images" : ["imagelink1", imagelink2]
}
```

Authentication required, will return an Article

Required fields: `title`, `description`, `body`

Optional fields: `tagList` as an array of Strings

### Update Article

`PUT /api/v1/articles/:slug`

Example request body:

```source-json
{
  "title": "Did you train your dragon?"
}
```

Authentication required, returns the updated Article

Optional fields: `title`, `description`, `body`

The `slug` also gets updated when the `title` is changed

### Delete Article

`DELETE /api/v1/articles/:slug`

Authentication required

### Like an Article

`PUT /api/v1/articles/:slug/like`

Authentication required

No additional parameters required
 
returns:

```
{
  "Message": "You have successfully liked this article"
}
```

doing the same for a second time returns:

```
{
  "Message": "You no longer like this article"
}
```

### Dislike an Article

`PUT /api/v1/articles/:slug/dislike`

Authentication required
No additional parameters required
 
returns:

```
{
  "Message": "You have successfully disliked this article"
}
```

doing the same for a second time returns:

```
{
  "Message": "You no longer dislike this article"
}
```

### Add Comments to an Article

`POST /api/v1/articles/:slug/comments`

Example request body:

```source-json
{
  "body": "His name was my name too."
}
```

Authentication required, returns the created Comment
Required field: `body`

### Get Comments from an Article

`GET /api/v1/articles/:slug/comments`

Authentication optional, returns multiple comments

### Like a Comment

`PUT /api/v1/articles/:slug/comments/:pk/like`

Authentication required

No additional parameters required
 
returns:

```
{
  "Message": "You have successfully liked this comment"
}
```

doing the same for a second time returns:

```
{
  "Message": "You no longer like this comment"
}
```

### Dislike a Comment

`PUT /api/v1/articles/:slug/comments/:pk/dislike`

Authentication required

No additional parameters required
 
returns:

```
{
  "Message": "You have successfully disliked this comment"
}
```

doing the same for a second time returns:

```
{
  "Message": "You no longer dislike this comment"
}
```

### Delete Comment

`DELETE /api/v1/articles/:slug/comments/:id`

Authentication required

### Edit Comment

`PUT /api/v1/articles/:slug/comments/:id`

Authentication required
Returns comment
Example Request Body:
```
{
  "content": "This is an edit to the original comment"
}
```

### Get comment edit history

`GET /api/v1/articles/:slug/comments/history/:id/`
Authentication required
No request params
Return body example:
```
[
    {
        "id": 3,
        "comment": "This is the original comment",
        "date_created": "2018-08-16T11:22:44.750507Z",
        "parent_comment": 1
    },
    {
        "id": 4,
        "comment": "This is the comment after first edit",
        "date_created": "2018-08-16T11:23:58.468756Z",
        "parent_comment": 1
    }
]
```

### Favorite Article

`POST /api/v1/articles/:slug/favorite`

Authentication required, returns the Article
No additional parameters required

### Unfavorite Article

`DELETE /api/v1/articles/:slug/favorite`

Authentication required, returns the Article

No additional parameters required

### View an Article's Ratings

`GET /api/v1/articles/:slug/ratings`

No authentication required, returns the Article's ratings

No additional parameters required

### Rate an Article

`POST /api/v1/articles/:slug/ratings`

Authentication required, returns the information of the user who just rated

Request body required:
```source-json
{
  "stars": 2
}
```
The number of stars should be 1,2,3,4 or 5.
An author cannot rate their own article

### Get Tags

`GET /api/v1/tags` _deprecated_

`GET /api/v1/articles/?tagList=<tag>`

### Configuring environment variables

* See the **.env-sample** file for the required environment variables needed to
setup the application
* Use this info to create a .env file
* Run `source .env` to initialize the environment variables

### Testing the application

* Run `coverage erase` to clear any residual coverage files.
* Run `coverage run manage.py test` to run the tests.
* Run `coverage report --include="authors/*" --skip-covered -m` to show the coverage report of your tests. 

  - Here, the `--include="authors/*"` ensures your report only reports on the coverage of the aurthors folder.
  - The `--skip-covered` ignores files with `100%`
    coverage.
  - The `-m` shows the missed lines.
