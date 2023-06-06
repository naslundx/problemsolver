cd frontend
npm run format
npm run lint
cd ..

cd backend/
black .
pylint .
