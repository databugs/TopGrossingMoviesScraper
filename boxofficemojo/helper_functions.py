
def cast_crew_base_url(movie_id: str) -> str:
    return f"https://www.boxofficemojo.com/title/{movie_id}/credits/?ref_=bo_tt_tab#tabs"

def clean_money_value(value: str) -> str:
    """
    Clean a money value by removing the "$" and "," characters.
    """
    return value.replace("$","").replace(",","")