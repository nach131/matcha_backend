# matcha_backend

### Tables structure:
```
users
├── id
├── username
├── email
├── first_name
├── last_name
├── password_hash
├── gender
├── sexual_preferences
├── biography
├── latitude
├── longitude
├── location
├── fame_rating
├── email_verified
├── last_login
└── created_at
```

```
tags
├── id
└── name
```

```
user_tags
├── user_id
└── tag_id
```

```
photos
├── id
├── user_id
├── path
├── is_profile
└── created_at
```

```
likes
├── id
├── from_user_id
├── to_user_id
└── created_at
```

```
profile_visits
├── id
├── visitor_id
├── visited_id
└── created_at
```
```
blocks
├── id
├── blocker_id
├── blocked_id
└── created_at
```

```
reports
├── id
├── reporter_id
├── reported_id
├── reason
└── created_at
```

```
messages
├── id
├── sender_id
├── receiver_id
├── content
├── read
└── created_at
```

```
notifications
├── id
├── user_id
├── type
├── related_user_id
├── read
└── created_at
```


### Docker commands:
```sh
    # docker build -t backend:1.0 .
    docker build <-t image-name> .

    # docker run -d -p 5100:5000 --name backend backend:1.0
    docker run <-d> <-p host_port:container_port> <--name container-name> <image-name>
```

### CURL tests:
For local HTTP development, start the app with `SESSION_COOKIE_SECURE=false`;
keep the default `true` when serving over HTTPS.

```sh
    # Log in with a username and password
    curl -c cookies.txt -X POST http://127.0.0.1:5100/api/v1/users/login \
        -H "Content-Type: application/json" \
        -d '{"username":"toma", "password":"tomate"}'

    # Get the authenticated user's profile
    curl -b cookies.txt http://127.0.0.1:5100/api/v1/users/me

    # Request a password reset code; check the backend logs for the code
    curl -X POST http://127.0.0.1:5100/api/v1/users/password-reset/request \
        -H "Content-Type: application/json" \
        -d '{"email":"toma@tomate.com"}'

    # Verify the reset code before showing the new-password form
    curl -X POST http://127.0.0.1:5100/api/v1/users/password-reset/verify \
        -H "Content-Type: application/json" \
        -d '{"email":"toma@tomate.com","code":"CODE_FROM_LOGS"}'

    # After verification, set the new password (the code is checked again)
    curl -X POST http://127.0.0.1:5100/api/v1/users/password-reset/confirm \
        -H "Content-Type: application/json" \
        -d '{"email":"toma@tomate.com","code":"CODE_FROM_LOGS","new_password":"new-password"}'

    # Get the top 10 suggested profiles (requires login)
    curl -b cookies.txt http://127.0.0.1:5100/api/v1/users/suggested

    # Get a user details
    curl -X GET http://127.0.0.1:5100/api/v1/users/get/test

    # Get all users that match the text "test"
    curl -X GET http://127.0.0.1:5100/api/v1/users/search/test

    # Get a user's photos and tags
    curl -b cookies.txt http://127.0.0.1:5100/api/v1/photos/by-user/1
    curl -b cookies.txt http://127.0.0.1:5100/api/v1/tags/by-user/1

    # Log out and invalidate the server-side session
    curl -b cookies.txt -c cookies.txt -X POST \
        http://127.0.0.1:5100/api/v1/users/logout

    # Create a user
    curl -X POST http://127.0.0.1:5100/api/v1/users/create \
        -H "Content-Type: application/json" \
        -d '{"username":"toma", "email":"toma@tomate.com", "password":"tomate", "gender":"verdura", "sexual_preferences":"otras verduras", "biography":"Soy una muy buena verdura", "latitude": 0.5, "longitude": 0.5}'

    curl -X POST http://127.0.0.1:5100/api/v1/users/create \
        -H "Content-Type: application/json" \
        -d '{"username":"test", "email":"test@testeado.com", "password":"tester", "gender":"testeador", "sexual_preferences":"otros testeadores", "biography":"Soy una muy buen testeador", "latitude": 1.5, "longitude": 1.5}'
```

User-associated resources can be listed with
`GET /api/v1/<resource>/by-user/<user_id>`. This includes photos, tags, user
tags, likes, messages, blocks, reports, notifications, and profile visits.
For resources that reference users in multiple roles, the endpoint returns
records involving the user in any of those roles.

Logging in creates a random session token, stores only its SHA-256 hash in
PostgreSQL, and sends the token in an HttpOnly, SameSite=Lax cookie. Sessions
expire after 30 minutes idle or 7 days absolute; logout revokes the database
session and clears the cookie. All resource GET and create endpoints require a
valid session. Signup, login, and public user profile/search endpoints remain
public. `SESSION_COOKIE_SECURE` defaults to `true`; set it to `false` only for
local HTTP development. Run `python -m app.database.schema` before serving
requests so the required database tables exist.

Password reset codes are one-time, expire after 15 minutes, and are logged
temporarily instead of being emailed; protect and inspect backend logs
accordingly. Suggestions exclude the current user and sort by shared tag count,
then distance, then fame rating, with a maximum of 10 profiles.
