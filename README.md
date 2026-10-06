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
'''sh
    docker build <-t image-name> .
    # example: docker build -t backend:1.0 .

    docker run <-d> <-p host_port:container_port> <--name container-name> <image-name>
    # example: docker run -d -p 5100:5000 --name backend backend:1.0
'''