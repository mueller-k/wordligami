# Wordligami

## Requirements

-- Ability to determine if a Wordle game board has been seen before
-- Determine when that board was last seen (all times seen before)
-- Determine who won the Wordle for that day? (time based review)

## Development

Utilizes a [Makefile](Makefile) for development scripts.

Run `make synth` to synth templates.

Run `make deploy` to deploy templates.

## Project To-Do

* Create data store for storing games
-- Storing users as well?
-- New data store per groupme chat (to support other chats)

* Create UI for displaying information about a submission
-- Site homepage lists all chats available
-- Can click into chat and see all submissions
-- Can click into submission and see if it's a Wordligami, or the last time the board was seen (and who submitted it)