# Groom Game Engine — Phase 1.5

The standalone engine is now connected to Flask.

## Test

Run your normal Flask application, then open:

`/game_engine/test/index.html`

Click **Create Temple Run Game**.

The API endpoint is:

`POST /api/game/create`

A successful response contains `game_id` and `game_url`.

## Important

This is the first integration step. The next step is to make Groom AI detect a
natural-language game request and call this endpoint/engine automatically.
After that, we will embed the playable game inside the Groom AI interface.
