#!/usr/bin/env python
# coding: utf-8

# In[32]:


from requests import get
url = 'https://www.rottentomatoes.com/top/bestofrt/?year=2019'
response = get(url,headers = {"Accept-Language": "en-US, en;q=0.5"})
print(response.text[:500])


# In[33]:


from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)


# In[104]:


movie_containers=html_soup.find_all('tr')
movie_containers = movie_containers[20:120]
print(movie_containers[0])


# In[132]:


first_movie = movie_containers[0]
first_name = first_movie.find('a',class_='unstyled articleLink')
first_name= first_name.text
print(first_name)
tomato1 = first_movie.find('span',class_='tMeterScore')
tomato1 = tomato1.text[:-1]
print(int(tomato1))
review1 = first_movie.find('td',class_="right hidden-xs")
review1 = int(review1.text)
print(review1)


# In[133]:


# Lists to store the scraped data in
names = []
tomatos = []
reviews = []
# Extract data from individual movie container
for container in movie_containers:
# If the movie has Metascore, then extract:
    #if container.find('a', class_ = 'unstyled articleLink') is not None:
    # The name
        name = container.find('a', class_ = 'unstyled articleLink').text
        names.append(name[2:])
    # The year
        #year = container.h3.find('span', class_ = 'lister-item-year').text
        #years.append(year)
    # The rating
        tomato = container.find('span',class_="tMeterScore").text[:-1]
        tomatos.append(int(tomato))
    # The Metascore
        review = container.find('td',class_="right hidden-xs").text
        reviews.append(int(review))
    # The number of votes
        #vote = container.find('span', attrs = {'name':'nv'})['data-value']
        #votes.append(int(vote))


# In[137]:


import pandas as pd
movie_ratings = pd.DataFrame({'movie': names,
'rating, %': tomatos,
'no. of reviews': reviews
})
movie_ratings.to_csv('movie_ratings.csv')

import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (16,4))
ax1, ax2, ax3 = fig.axes
ax1.hist(movie_ratings['rating, %'], bins = 10, range = (0,100)) # bin range = 1
ax1.set_title('Rotten Tomatoes rating, %')
ax2.hist(movie_ratings['no. of reviews'], bins = 10, range = (0,100)) # bin range = 10
ax2.set_title('No. of reviews')
ax3.hist(movie_ratings['rating, %'], bins = 10, range = (0,100), histtype = 'step')
ax3.hist(movie_ratings['no. of reviews'], bins = 10, range = (0,100), histtype = 'step')
ax3.legend(loc = 'upper left')
ax3.set_title('Ratings + Number of reviews')
for ax in fig.axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
plt.show()


# In[ ]:




