# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

```bash
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:
```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:
```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```

## Where to Start

1. **Read `planning.md` and fill it out before writing any code.**
2. Verify the data loads correctly by running `python utils/data_loader.py`.
3. Build and test each tool individually before connecting them through your planning loop.

Your implementation files go in this same directory. There's no required file structure for your agent code — organize it however makes sense for your design.

## Testing Individual Tool Failure 
1. Trigger `search_listings` returning zero results
   - Input: 
    ``` 
    python -c "from tools import search_listings; print(search_listings('designer ballgown', size='XXS', max_price=5))"
    ```
   - Output: 
   
   ![alt text](image-4.png)

2. Trigger `suggest_outfit ` returning empty wardrobe
   - Input: 
    ``` 
    python -c "
    from tools import search_listings, suggest_outfit
    from utils.data_loader import get_example_wardrobe, get_empty_wardrobe
    results = search_listings('vintage graphic tee', size=None, max_price=50)
    print(suggest_outfit(results[0], get_empty_wardrobe()))
    "
    ```
   - Output: 
   
    ![alt text](image-2.png)

3. Trigger `create_fit_card  ` with empty outfit string:
   - Input: 
    ``` 
    python -c "
    from tools import search_listings, create_fit_card
    results = search_listings('vintage graphic tee', size=None, max_price=50)
    print(create_fit_card('', results[0]))
    "
    ```
   - Output: 
   
    ![alt text](image-3.png)