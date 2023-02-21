# Box Office Mojo Scraper
A Python Scrapy spider to scrape the worldwide top lifetime grossing movies from Box Office Mojo and extract their cast and crew details.

## Installation
1. Clone this repository: git clone https://github.com/databugs/boxofficemojo-scraper.git
2. Install the required packages: ```pip install -r requirements.txt```

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
- Movie URL
- Movie ID

For each movie, the spider will follow its URL to extract the following details for its cast and crew:

- Name
- Role
- ID

The extracted data will be saved in JSON format in the output.json file.