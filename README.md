# Instructions
1. Install python 3.8.x
2. pip install pipenv 
`pip install pipenv`
3. Create environment using pipenv
`pipenv install`
4. Activate environment
`pipenv shell`
5. cd in django project directory
`cd bink`
6. Run project locally
`python manage.py runserver 0:8000`
This will warn you about unapplied migrations but for this example it's not needed.
7. Navigate to `localhost:8000/phone-mast`
8. Click on links to display the day on the page and console.


## Running tests
`pytest`

## Lint
`flake8`

## Future changes
- Have the ability to allow users to upload a CSV file.