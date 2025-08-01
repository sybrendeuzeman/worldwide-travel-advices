# Rough idea 

How to collect all travel advices from goverment

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
- [UK](https://www.gov.uk/foreign-travel-advice)
    - Website is [open source](https://github.com/alphagov/travel-advice-publisher) (good for the UK!!!). The website uses an [API](https://github.com/alphagov/travel-advice-publisher/blob/main/docs/further_technical_information.md). We should be able to reverse engineer this!
- [USA](https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html/)


