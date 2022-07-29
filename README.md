# Food Delivery Backend

This is a food delivery backend service that uses Flask for the API layer. It uses patterns from
[Architecture Patterns with Python](http://www.cosmicpython.com/book/preface.html) which is quite
good and will make it easier to migrate from a monolith to microservices later.

## Quickstart

At a high level:

1. `make build`
1. `make shell`
1. `make migrate`
1. `make server`
1. Open a new terminal with `make bash`
1. `make data`

## Getting started

Make sure docker is running.

```bash
$ # build the container
$ make build
$ # enter the container with a bash shell
$ make shell
$
root@b9ac6f3f4c66:/code # Now you're in the container!
root@b9ac6f3f4c66:/code # Setup your database tables
root@b9ac6f3f4c66:/code make migrate
root@b9ac6f3f4c66:/code # You should see output and no errors.
root@b9ac6f3f4c66:/code # Run the API server
root@b9ac6f3f4c66:/code make server
flask run --reload --host 0.0.0.0
 * Serving Flask app '/code/src/main.py' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
 * Running on http://172.19.0.3:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 137-642-367
```

Now that the server is running in the container, insert some test data. In a _different_ terminal
window, open up another shell to the container (remember, the server should still be running from
the `make server` command above)

```
brianz@(main=)$ make bash
docker exec -it \
		`docker ps -f name=manning-eda-food-delivery-backend_web --format "{{.ID}}"` bash
root@2beedcf1d752:/code# # You're in the container now with a different shell!
root@2beedcf1d752:/code# make data
root@2beedcf1d752:/code# .... lots of output
```

Now you have menu items, orders, etc. to play with via the API.

## Postman

The API is available on your host machine on port 5150. Use a Postman environment with a `HOST`
variable with the value `http://localhost:5150`

## Secrets

This setup needs sensitive variables which are stored in an `envs/secret.env` file. _This file is
ignored in git!_ The contents are made known to special people via Slack. Without the `secret.env`
file, things won't work, such as publishing to EventBridge.

## Notes

- All of the code worth looking at is in the `foodie2ue` directory
- The API routes are defined in `foodie2ue/api/routes.py`. You can see the API routes and how they
  map to code at the very bottom of that file in a function called `connect_routes`.
- This code would be much simpler without these patterns in place. However, simpler code would be
  harder to extract later.
- There are no tests yet, mostly b/c all this is doing is creating and reading data. Add business
  logic arrives, we can add tests.
