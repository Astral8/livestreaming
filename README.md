# Livestreaming App

This serves as a website that hosts static files as well as the ability to livestream.

The site is hosted through Heroku at: [CNT Livestreaming App](https://cnt-livestreaming-app.herokuapp.com/)

## About

This site was created as a project for CNT4713.

It was intended to be a site created through [Python](https://www.python.org/) and [Flask](https://flask.palletsprojects.com/en/2.0.x/).

It required the following features:
* A login screen for authentication.
* Code hosted in a cloud provider.
* A sample static feed.
* A sample live feed.

## Login

The Login was done through mainly the Authlib package for Python. First [Google API Credentials](https://cloud.google.com/apis) were set up so a user could login safely through Google. From there [OAuth](https://oauth.net/2/) and [OpenID Connect Client](https://openid.net/) were set up.

Essentially, a user would login through Google, then OpenID would handle the creation of a token, and then a user dict was created and implemented into a session. 

This also guarantees more security for the site as the pages are protected behind requiring a user to be logged in through Google.

Once a user is done with the site, they can press the logout button which will remove the user from the session and redirect them to the landing page.

## Heroku

The Code was hosted on [Heroku](https://www.heroku.com/) and linked to this Github Repo. This way anytime that a branch was merged, Heroku would automatically deploy an updated version of the site.

## Sample Static Feed

One of the pages for the site holds a sample static feed. The videos are hosted on the Heroku server, and can be viewed directly on the site.

One of the videos is a 30 second clip that was initally the only video on the page and meant to represent the sample static feed as it would buffer. However since it was a short clip it would often load fully immediately. As a result, another video was added.

The other video not only better displays the videos buffering but also explains how exactly the livestream works.

## Sample Live Feed

The sample live feed is a livestream utilized through ngrok and opencv2. 

[OpenCV2](https://opencv.org/) essentially lets the user create a livestream through a continuous stream of images. Although there is no audio, it is still a better implementation that other possibilities that were looked up. 

[ngrok](https://ngrok.com/) is used in order for the user to host their stream to the site. This is done by opening the website on a local server, then they can open up ngrok and tunnel their localhost through an ngrok link. The ngrok link is added to the github repo and causes Heroku to automatically redeploy the site. After that, the livestream page will then call upon the ngrok link letting the user livestream from their local machine to anyone else who is on the website.
