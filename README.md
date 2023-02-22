# Box Office Mojo Scraper
A Python Scrapy spider to scrape the worldwide top lifetime grossing movies from Box Office Mojo and extract their cast and crew details.

## Installation
1. Clone this repository: git clone https://github.com/databugs/TopGrossingMoviesScraper.git
2. Create and activate a virtual environment
3. Install the required packages: ```pip install -r requirements.txt```

## Usage
Run the spider using the following command: 
```scrapy crawl boxofficemojo```

The spider will scrape the data and save it in output.json file in the project directory.

## Output
The spider will extract the following details for each movie:

- Title
- Worldwide lifetime gross
- Domestic lifetime gross
- International lifetime gross
- Year
- Rank
- Movie URL (relative url)
- Movie ID

For each movie, the spider will follow its URL to extract the following details for its cast and crew:

- Name
- Role
- ID

The extracted data will be saved in JSON format in the `topgrossingmovies.json` file, and in the `/data/` folder.

## Workflow
The GitHub Actions workflow will run on a schedule and perform the following steps:

1.  Checkout the repository's content
2.  Set up Python with version 3.10
3.  Install dependencies using pip
4.  Fetch the top grossing movies by running the `boxofficemojo` spider
5.  Commit and push changes to the repository if the data has changed

The workflow is scheduled to run every day at 12:49 AM UTC.
