from src.tools.tools import web_search,scrape_web
from rich import print


result = scrape_web.invoke(" https://ai.cornell.edu/category/featured")
print(result)
