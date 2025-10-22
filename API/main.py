from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="")

schema = {
    "type": "object",
    "properties": {"model": {"type": "string"},
                   "release_date": {"type": "string"},
                   "display": {"type": "string"},
                   "battery": {"type": "string"},
                   "camera": {"type": "string"},
                   "RAM": {"type": "string"},
                   "storage": {"type": "string"},
                   "price": {"type": "string"}},
    "required": ["model", "release_date", "display", "battery", "camera", "RAM", "storage", "price"],
}

res = firecrawl.extract(
    urls=["https://m.gsmarena.com/samsung_galaxy_a17-14157.php"],
    prompt="get  model name, release date,display, battery, camera, RAM, storage, and price",
    schema=schema,
)
print(res.data)
print(res)
