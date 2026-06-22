# auth-licence

A tiny Python library that records anti‑piracy incidents, persists them to SQLite,
and lets an admin disable users. It mimics a Redis cache with an in‑memory
dictionary, making it easy to test without external services.

## Features

- **Add incident** – timestamp, user, IP, and reason are stored.
- **List incidents** – ordered by timestamp.
- **Disable user** – mark a user as disabled; query the status.
- **Persistence** – incidents and disabled users are saved in a SQLite file
  while also being kept in a Redis‑like in‑memory store.

## Installation
