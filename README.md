# Podcasts

## About

Users of the Podcast app can search for a podcast, browse top ten categories based on iTunes ratings, play episodes, and store a list of their favorite podcasts in a database. Navigation occurs by clicking on the icons along the bottom of the screen.

### Features

- HTML5 audio player
- RSS parsing
- iTunes podcast feed
- CSS Flexbox layout

### Built With

- Vue – A JavaScript framework used to build the user interface
- Python/Flask server – Used to serve the API endpoints to the front end and facilitate conversation between the database and Vue
- SQLAlchemy – Used to facilitate communication between Python and the database
- Amazon Relational Database Service (RDS) PostgreSQL (Postgres) database – Used to configure the database and for SQL and JSON querying of the database
- SQLite3 database – Used to configure and query the database when using a localhost
- rss-parser – Library used to parse RSS XML feeds into JavaScript objects

## Installation

### Getting Started

1. Fork the github repo
2. Install Dependencies (see [Installing Dependencies](https://github.com/krskelton/podcasts#installing-dependencies) for details)
3. Create an AWS account and add an RDS database instance. (see [Configuring the Database](https://github.com/krskelton/podcasts#configuring-the-database) for details on setup)
4. Create .env file to contain database information in the Server file (see [Environment Variable Configuration](https://github.com/krskelton/podcasts#environment-variable-configuration) for details).
5. Run the app. (see [Running Locally](https://github.com/krskelton/podcasts#running-locally) for details)

### Prerequisites

- NodeJS v10.16.3
- Python 3.7+
- Pipenv
- SQL database – I used AWS RDS PostgreSQL
- sqlite3 (for local db)

### Installing Dependencies

Navigate into the Client folder and install npm.

`npm install`
`npm install sugar`
`npm install vue-router`

Navigate into the Server folder and install pipenv.

`pipenv install`

## Deployment Configuration

### Configuring the Database

**Network DB**

- Create your AWS account.
- Under Services, choose Relational Database Service (RDS).
- Follow this guide to set up an RDS DB instance.
- Update your .env file with the appropriate DB values.
- Make sure that the RUN_ENVIRONMENT in the .env file is ‘network’

**Local DB**

- In the .env file, change the RUN_ENVIRONMENT to ‘local’

### Environment Variable Configuration

Navigate to the Server file and create a .env file with the following information:
DB_PASS= ‘insert your data'
DB_URL=‘insert your data'
DB_NAME=‘insert your data'
RUN_ENVIRONMENT=‘insert your data'

### Running Locally

- In a terminal window open two tabs:
  - In one tab, navigate into the Client folder and enter:
    - `npm run build`
  - In the other tab, navigate into the Server folder and enter:
    - `pipenv run python main.py`
- Navigate to https://localhost:5000/ (or specified address in terminal) on your browser

## Caveats and Good-To-Knows

- The call to the iTunes API can be slow at times, especially for the Browse functionality.

## Next Steps

### Planned Features:

- User accounts
- Subscription thank you message
- Disabled subscription button when a user is already subscribed
- Count of episodes the user has listened to in subscription list
- Add play icon at the bottom with
