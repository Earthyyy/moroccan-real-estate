# Scraping Module

## Introduction

Web scraping is our go-to technique for collecting data from different real estate platforms.

We are focusing on collecting data about appartments on sale throughout Morocco.

The main platforms used for data collection are:

- [Avito](https://www.avito.ma/)
- [Yakeey](https://yakeey.com/fr-ma)

The following is a description regarding practices and rules we followed while scraping data, as well as the limitations and challenges faced for each platform.

## Avito

[Avito](https://www.avito.ma/) is a large marketplace that provide a wide range of products in every category. But as real estate is a very large category on its own, the platform dedicated resources made specifically for this class of products.

In our case, we are going to be looking at [appartments for sale](https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre), which currently contains more than 47k annoucements, making it our biggest data source.

### Description

- Each page contains about 44 announcements, with more than 1400 pages.
- A page is estimated to take about 5 seconds to be scraped.

### Rules

- The [robots.txt](https://www.avito.ma/robots.txt) file doesn't seem to contain rules that forbid the use of automated bots for retrieving data. However, considering the large ammount of data to be collected, we have to be very careful not to disturb the traffic.

### Challenges

- Huge number of requests to be made.
- Premium announcements are JavaScript rendered (2 per page).
- Description is not fully displayed, and requires a click to be shown.
- Retrieving Javascript rendered attributes, such as the number of rooms, bathrooms, etc (represented by icons):

![JS rendered](../../images/avito_js_rendered.png)

- Some announcement links redirect to external websites:

![External redirection](../../images/avito_external_redirection.png)

- Extracted text is not always clean, some characters are replaced by their HTML entities, and arabic text is not displayed correclty.

### Suggestions

- On scraping settings, we have set the download delay to 0.5 second.
- Fortunately, we can extract JS rendered information from the announcements list page, as the information is displayed directly there and it is easier to process it. Here's how the information is displayed:

![JS rendered](../../images/avito_announcement_list.png)

- We can easily distinguish between internal and external websites (scrapy does this automatically via the allowed_domains attribute of the scrapper), making it easy to ignore those external redirections.

## Yakeey

[Yakeey](https://yakeey.com/) is a marketplace specialized in real estate products in all categories (rent, sale, etc).

We will get the desired data from the [appartments for sale](https://yakeey.com/fr-ma/achat/appartement/maroc) category, which is expected to contain a bit more than 800 announcements.

However, because this platform only deals with real estate, the data is expected to be more reliable with a high quality. the reason is because before any announcement is posted, it is visited by real estate consultants who verify the information and approve the announcement. This means that we should expect a very low chance of an error while scraping the data.

### Description [Yakeey]

- Each page contains 25 announcements, with more than 33 pages.
- For each page, we can expect 18 regular announcements, with an optional 5 locked announcements (not verified by the platform) and an optional 2 announcements for new projects.

### Rules [Yakeey]

- Again, the [robots.txt](https://yakeey.com/robots.txt) file doesn't seem to contain rules that forbid the use of automated bots for retrieving data.

### Challenges [Yakeey]

- The platform is very reliable, and the data is very clean and well structured.
- Here are the types of announcements we can expect to find:

![Regular](../../images/yakeey_regular.png)

![Locked](../../images/yakeey_locked.png)

![New project](../../images/yakeey_new_project.png)

- Each regular announcement contains three main sections:
  - header: title, reference, neighborhood, etc.
  - Attributes: number of rooms, bathrooms, etc.
  - Equipments: air conditioning, heating, etc.
- Some information is not available directly in HTML, but there is a workaround to get it from the announcements listing page.
- There is no record for the time of the announcement.

### Suggestions [Yakeey]

- We are only interested on the regular type of announcements, locked ones will be transformed into regular ones after verification.
- We are going to use the `reference` attribute of the announcement to know if we have already processed it or not. This is because there is no actual record for the time. However, we can guarantee the order of the announcements, as well as the uniqueness of the reference, meaning that as soon as we reach an announcement with a reference that we have already processed, we can stop the process.
