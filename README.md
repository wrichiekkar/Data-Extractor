# Data Extractor

These extractors were designed to extract data from Siteimprove (analytics SaaS) as there was no API available. Used selenium to extract issues and their occurences.

Selenium was used as opposed to other modules such as request and mechanize as the login featured OpenID Connect, which other modules were not able to bypass. 


EX: Collect "Image with no attribute" across 1800 pages. The amount of accessibility issues vary and the scripts collect all issues on the page itself after it has fully loaded.

## Alt Link Extractor

**Image link is missing alternative text**<br>
The image link is missing an alternative text stating the purpose of the link.<br>
<strong>How to fix it:</strong><br>
If for instance it links to a web page, state the topic of that page.

## Alt Text Extractor
**Image with no alt attribute**<br>
The image does not have an 'alt' attribute (alt="").<br>
<strong>How to fix it:</strong><br>
It’s important all images have the attribute for alternative text regardless of whether an alternative text is added.
A screen reader knows how to handle both an empty alt attribute and one with a text. If there is no attribute some screen readers will compensate and read the path to the image instead which will often give no value to the end user.

## Bold Tag Extractor
**"Bold" tag used to format text** <br>
The 'bold' tag is used to highlight text.<br>
<strong>How to fix it:</strong><br>
Consider the following: If the text should be emphasized semantically, use the 'strong' tag instead. If the text is a heading, an 'H' tag (such as H1, H2, H3...) should be used instead. If the text is highlighted as a visual effect, CSS should be used to do this.

## I Tag Extractor
**"i" tag used to format text**<br>
The italics-tag 'i' is used to highlight text.<br>
<strong>How to fix it:</strong><br>
If the text should be emphasized semantically, use the 'emphasize' tag instead. If the text is a heading, an H-tag (such as H1, H2, H3...) should be used instead. If the text is highlighted as a visual effect, CSS should be used to do this.

Please note that even though 'i' tags are commonly used for inserting icons, this is considered bad practice.

## Iframe Extractor
**iFrame is missing a title**<br>
The iFrame has no 'title' attribute or the 'title' attribute is empty.<br>
<strong>How to fix it:</strong><br>
Provide the frame with the attribute title=”” and add a description of the content in the title.
