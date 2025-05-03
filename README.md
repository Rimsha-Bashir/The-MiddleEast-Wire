## The MiddleEast Wire: A Web Scraping-Powered News Aggregator 🌐

### Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Run the Project](#run-the-project)
- [Application Preview](#application-preview)

### Overview 🔭

The MiddleEast Wire is a curated collection of the latest news articles from around the world, with a strong focus on the Middle Eastern coverage. It extracts content from leading sources like <i>Middle East Eye</i> and <i>Al Jazeera</i>, presenting them in a clean, searchable interface.

### Features 🧬

1. <b>News Scraping & Display:</b> The app scrapes articles from news sources, stores them in an SQLite database, and dynamically displays them with details like title, source, and image.

2. <b>Filtering Options:</b> Users can filter articles based on source, keywords, and topics through a form that updates the displayed results in real-time.

3. <b>Responsive UI:</b> Built with Flask and Bootstrap, the app features a responsive design for viewing articles across different devices.

4. <b>Database Management:</b> Articles are stored in an SQLite database, which is queried to retrieve and display filtered articles, with error handling for failed scraping attempts.


### Tech Stack ⚙️

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-%23ffffff.svg?style=for-the-badge)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

### Run the project 🚀

1. Create a py venv.

```bash 
py -3 -m venv .venv
```

2. Activate the venv

```bash 
source venv/Scripts/activate
```

3. Install Flask with pip 

```bash 
pip install -r requirements.txt
```

4. Run the flask application

```bash
py newsapp.py 
```

### Application Preview 📑

A responsive Flask web application displaying news articles from the Middle East, featuring Source, Topic, Keyword and Date filters, along with paginated results.

![Image 1](images/newsapp1.PNG)

![Image 2](images/newsapp2.PNG)

![Image 3](images/newsapp3.PNG)