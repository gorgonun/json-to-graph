#! /bin/bash

mongoimport --collection "$MONGO_SEED_MONGODB_COLLECTION" --type json --file /mongo-seed/nyt-example.json --jsonArray "$MONGO_SEED_MONGODB_URL"