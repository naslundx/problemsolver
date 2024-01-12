yarn run format
yarn run lint

cd backend/
black .
pylint .
