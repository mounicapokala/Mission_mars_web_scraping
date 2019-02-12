from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from selenium import webdriver

def scrape():
    nasa_url = "https://mars.nasa.gov/news/"
    nasa_browser = webdriver.Chrome()
    nasa_browser.get(nasa_url)
    nasa_rendered = nasa_browser.execute_script("return document.body.innerHTML")
    soup_nasa = BeautifulSoup(nasa_rendered,'html.parser')

    #Nasa Mars latest news
    nasa_div_tag = soup_nasa.find('div',class_='image_and_description_container')
    nasa_latest_title = nasa_div_tag.find('h3').text
    #Nasa paragraph
    nasa_paragraph = soup_nasa.find('div',class_='rollover_description_inner').text

    #JPL Mars space images
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    jpl_home_url = "https://www.jpl.nasa.gov"
    response_jpl = requests.get(jpl_url)
    soup_jpl = BeautifulSoup(response_jpl.text,'html.parser')

    jpl_class = soup_jpl.find('article',class_='carousel_item')
    jpl_style = jpl_class["style"]
    jpl_scrape_image = jpl_style[23:][:-3]
    jpl_full_image = jpl_home_url+jpl_scrape_image

    #Mars weather
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    response_weather = requests.get(mars_weather_url)
    soup_weather = BeautifulSoup(response_weather.text,'html.parser')

    mars_weather = soup_weather.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    #print(mars_weather)

    #Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url,header=None)

    #Mars Hemispheres
    hemisphere_list = ['cerberus_enhanced','schiaparelli_enhanced','syrtis_major_enhanced','valles_marineris_enhanced']
    hemisphere_img_url = []
    hemisphere_base_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/'
    usgs_home_url = 'https://astrogeology.usgs.gov'
    hemi_dict = {}
    for hemisphere in hemisphere_list:
        hemisphere_url = hemisphere_base_url+hemisphere
        response = requests.get(hemisphere_url)
        soup = BeautifulSoup(response.text,'html.parser')
        hemi_img = soup.find('img',class_='wide-image')
        hemi_img_url = usgs_home_url+hemi_img['src']
        hemisphere_title = soup.find('h2',class_='title').text
        hemi_dict['title'] = hemisphere_title
        hemi_dict['img_url']= hemi_img_url
        hemisphere_img_url.append(dict(hemi_dict))
    
    #print(hemisphere_img_url)

    mars_dict = {}
    mars_dict['news_title'] = nasa_latest_title
    mars_dict['news_p'] = nasa_paragraph
    mars_dict['featured_image_url'] = jpl_full_image
    mars_dict['mars_weather'] = mars_weather
    for df in tables:
        df.columns = ['col1','col2']
        mars_dict['mars_facts_table'] = df.to_dict(orient = 'records')
    mars_dict['hemisphere_image_url'] = hemisphere_img_url

    return mars_dict



mars_info_dict = {}
mars_info_dict = scrape()   
for key,value in mars_info_dict.items():
   print (f"{key} : {value}")




