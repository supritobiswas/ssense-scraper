# SSENSE Scraper

This is a Python script designed to scrape product data and images from [SSENSE](https://www.ssense.com/) website. 

## About SSENSE

SSENSE is a Montreal-based fashion platform that offers a curated selection of luxury and streetwear brands for both men and women. The website features a wide range of products including clothing, shoes, bags, and accessories from popular designers like Gucci, Saint Laurent, and Balenciaga.

## Functionality

This script can be used to scrape product data and images from SSENSE. The script uses Python and the BeautifulSoup library to navigate the website and extract relevant information. The scraped data is then saved to a CSV file.

The script can be customized to scrape specific categories or products by modifying the URL input. 

## Getting Started

To use this script, you will need to have Python 3.x installed on your machine along with the following libraries:

- requests
- BeautifulSoup
- csv

To install these libraries, you can use pip by running the following command:

`pip install requests BeautifulSoup csv`

## Usage

To use this script, you will need to run the following command in your terminal:

`python ssense_scraper.py`


The script will prompt you to enter a URL for the products you want to scrape. Once you enter the URL, the script will scrape the product data and images and save them to a CSV file.

## Disclaimer

Please note that web scraping may be against the terms of service of some websites. It is your responsibility to ensure that your use of this script complies with the terms of service of SSENSE.
