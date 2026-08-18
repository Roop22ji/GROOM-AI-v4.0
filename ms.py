from duckduckgo_search import DDGS

with DDGS() as ddgs:
    results = list(ddgs.text("Python programming", max_results=3))

for r in results:
    print(r)