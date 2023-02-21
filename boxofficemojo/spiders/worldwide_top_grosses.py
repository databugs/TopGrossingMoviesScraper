import scrapy
from boxofficemojo.items import MovieItem, CrewItem, CastItem, MovieDetails
from boxofficemojo.helper_functions import cast_crew_base_url, clean_money_value

class BoxOfficeMojoSpider(scrapy.Spider):
    """
    A spider to scrape the worldwide top lifetime grossing movies from Box Office Mojo.
    """
    name = "boxofficemojo"
    allowed_domains = ["boxofficemojo.com"]
    start_urls = ["https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?area=XWW"]
    
    custom_settings = {
                        "FEEDS": {
                            "data/topgrossingmovies.json": {
                                "format": "json",
                                "encoding": "utf8",
                                "store_empty": False,
                                "fields": None,
                                "indent": 4,
                            }
                        },
                    }

    
    def parse(self, response)-> dict:
        """
        Parse the response to extract movie details and follow pagination links.

        Args:
            response: The response of the request made.

        Yields:
            A dictionary containing the movie details as key-value pairs.
        """
        rows = response.css("tr")[1:]
        for row in rows:
            title = row.css(".mojo-field-type-title .a-link-normal::text").get()
            worldwide_lifetime_gross, domestic_lifetime_gross, international_lifetime_gross = [clean_money_value(item) for item in row.css(".mojo-field-type-money::text").extract()]
            year = row.css('.mojo-field-type-year .a-link-normal::text, .mojo-field-type-year:not(:has(a))::text').extract_first(default='')
            rank = row.css(".mojo-field-type-rank::text").get().strip()
            movie_url = row.css(".mojo-field-type-title a::attr(href)").get()
            movie_id = row.css(".mojo-field-type-title a::attr(href)").get().split("/")[2]

            movie = MovieItem(
                title=title, 
                worldwide_lifetime_gross=worldwide_lifetime_gross,
                domestic_lifetime_gross=domestic_lifetime_gross,
                international_lifetime_gross=international_lifetime_gross, 
                year=year, 
                rank=rank,
                movie_url=movie_url,
                movie_id=movie_id
                )
            # Follow the movie URL to parse the cast and crew data
            
            cast_crew_url = cast_crew_base_url(movie_id)
            
            yield response.follow(url=cast_crew_url, callback=self.parse_movie_page, meta={"movie": movie})
            
        # Follow pagination links
        has_next_page = response.css(".a-last a::attr(href)").get()
        if has_next_page:
            next_page_url = response.urljoin(has_next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
            
    def parse_movie_page(self, response):
        """
        Parse the response to extract the cast and crew data.

        Args:
            response: The response of the request made.

        Yields:
            A dictionary containing the cast and crew details as key-value pairs.
        """
        # Retrieve the movie item from the response's metadata
        movie: MovieItem = response.meta["movie"] 
        
        # Extract the crew information
        crew_name = response.css("#principalCrew td .a-link-normal::text").extract()
        
        crew_role = response.css("#principalCrew td + td::text").extract()
        crew_id = [item.split("/")[4] for item in response.css("#principalCrew td a::attr(href)").extract()]
        
        items: list = [movie]
        
        # Initialize the list hold all crew and cast items
    
        crew_items: list = []
        # Create a CrewItem object for each member of the crew
        for member in zip(crew_name, crew_role, crew_id):
            name, role, id = member
            crew = CrewItem(
                crew_id=id,
                role=role,
                name=name
            )
            crew_items.append(crew)
            
        cast_items: list = []
        # Extract the cast information
        cast_name = response.css("#principalCast td .a-link-normal::text").extract()
        cast_role = response.css("#principalCast td + td .a-expander-partial-collapse-content::text").extract()
        cast_id = [url.split("/")[4]  for url in response.css("#principalCast td a::attr(href)").extract() if url.startswith("http")]  
        
        # Create a CastItem object for each member of the cast
        for member in zip(cast_name, cast_role, cast_id):
            name, role, id = member
            cast = CastItem(
                cast_id=id,
                role=role,
                name=name
            )
            
            cast_items.append(cast)
            
        movie_details = MovieDetails(
            id=movie.movie_id,
            info=movie,
            crew=crew_items,
            cast=cast_items
        )
    
        yield movie_details