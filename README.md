# Food Delivery Backend

This is a food delivery backend service which is based on Flask. It uses patterns from
[Architecture Patterns with Python](http://www.cosmicpython.com/book/preface.html) which is quite
good and will make it easier to migrate from a monolith to microservices later.

## Quickstart

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

The API is available on your host machine on port 5150. Load the Postman collection _and_
environment which is in the `/postman` directory, in the repo.

- Create a copule of `MenuItems`
- Create a few `AddOns` for one or more `MenuItems`
- List the `MenuItems`

## Notes

- All of the code worth looking at is in the `foodie2ue` directory
- The API routes are defined in `foodie2ue/api/routes.py`. You can see the API routes and how they
  map to code at the very bottom of that file in a function called `connect_routes`.
- This code would be much simpler without these patterns in place. However, simpler code would be
  harder to extract later.
- There are no tests yet, mostly b/c all this is doing is creating and reading data. Add business
  logic arrives, we can add tests.
