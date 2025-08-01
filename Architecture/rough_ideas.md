# Rough idea 

We need to collect the data, harmonize it and then visualize it. Preferably as automatic as possible.

## In general

In general, I want to use Python to collect the data and also setup a database (basically the tool I know)
- At first, I will work with a nice SQLite-database. Using SQLalchemy we can make sure we can relatively easily use another type of database, ensuring flexibility.

## Collection
Governments do not all adhere to the same standards when providing travel advices. Within the collection phase, we therefore probably need many different scripts that collect travel advices from many different places and transform these in one unified format that can be used throughout.

In the end, we should also make sure we collect historic data. This phase, however, will focus on collecting a snapshot (and we deal with history later).

### Unified format
A quick look at a few governments providing travel advices suggest the following format: 

In general travel advices consist of two levels: one or multiple labels summarizing the safety and information on various aspects. 

- table advice labels
    - Country code of advising county (ISO 3166)
    - Country name advice (as provided by government)
    - Country code (ISO 3166, probably need to add this in scraping / collecting)
    - Label category (general, and advising country specific).
        - I can imagine countries provide multiple labels. We should at least collect a 'general' label, but collect other labels as well. For these, harmonizing should happen at a later stage.
    - Label
        - At this stage, use the categories as provided by the government. We will harmonize these in a later stage (if possible).

- table advice information
    - Country code of advising county (ISO 3166)
    - Country code (ISO 3166, probably need to add this in scraping / collecting)
    - Information category
    - Information

### First collection candidates
We can start with a few countries, also to test what the unified format can look like. 

- [Netherlands](https://www.nederlandwereldwijd.nl/reisadvies)
    - My country, so lets feed my patriotism
    - I can feed my nationalism by there being an [API](https://apis.developer.overheid.nl/apis/minbz-nederland-wereldwijd#:~:text=Nederland%20Wereldwijd%20Open%20Data%20API,en%20hulp%2Dbij%2Dnood.)!!!
- [UK](https://www.gov.uk/foreign-travel-advice)
    - Website is [open source](https://github.com/alphagov/travel-advice-publisher) (good for the UK!!!). The website uses an [API](https://github.com/alphagov/travel-advice-publisher/blob/main/docs/further_technical_information.md). We should be able to reverse engineer this!
- [USA](https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html/)
    - Mweh, why not the empire as well. Seems at least doable.

## Unified database
In the basis we can use the same tables as in collection. 
- To build a historic collection, we can add a date of collection and indicator whether this is the last data collected from the specific government.
- We should add a table with information on ISO 3166 country codes.
- A table translating the labels from each government into a harmonized framework. 
- Add an AI-translation of information provided by each government (?)

## Visualization
We have a database and after that we can think of many, many ways to visualize the data :).
