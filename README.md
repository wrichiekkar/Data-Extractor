# Data Extractor

These extractors were designed to extract data from Siteimprove (analytics SaaS) as there was no API available. Used selenium to extract issues and their occurences.

Selenium was used as opposed to other modules such as request and mechanize as the login featured OpenID Connect, which other modules were not able to bypass. 


EX: Collect "Image with no attribute" across 1800 pages. The amount of accessibility issues vary and the scripts collect all issues on the page itself after it has fully loaded.
