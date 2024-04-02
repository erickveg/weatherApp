# API &#8614; DATA &#8614; DASHBOARD

We use APIs to digest streaming data, and this challenge will require you to figure out an API and then build the data from that API into your Dashboard. Our current challenge is the [OpenWeatherMap API](https://openweathermap.org/). We learned about [Streamlit] (https://streamlit.io/) and [Docker] (https://www.docker.com/) for application development. We will build an app that uses the API to display weather data for decision-making.

## Coding Challenge

### Driving needs

_Each of the items below must be addressed by your app._

1. Provide a process for users to input their API key.
2. Allow the user to pull data for the three BYU locations for their selected month in the last six months. Use the [history data API](https://openweathermap.org/history)
3. Display a table of historical weather data for all three cities that includes;
    - The average daily high temperature for the month.   
    - The average daily low temperature for the month.   
    - The number of observations at each location.   
    - The number of hours in the month the temperature is above a user input value.
5. Multiple visualizations/tables.
    - Daily highs over the month for each location.   
    - A visualization that uses boxplots to show each city's varied hourly temperature readings.   
6. An additional interactive element that allows the user to investigate the visualizations.

### Data Science Dashboard

We will use Streamlit as our prototype dashboard tool, but we need to embed that streamlit app into a Docker container.

Within this repository you can simply run `docker compose up` to leverage the `docker-compose.yaml` with your local folder synced with the container folder where the streamlit app is runnning. 

Additionally, you can use `docker build -t streamlit .` to use the `Dockerfile` to build the image and then use `docker run -p 8501:8501 -v "$(pwd):/app:rw" streamlit` to start the container with the appropriate port and volume settings.

### Repo Structure

Your repo should be built so that I can clone the repo and run the Docker command (`docker compose up`) as described in your `readme.md` that allows me to see your app in my web browser without requiring me to install Streamlit on my computer.

1. Fork this repo to your private space
2. Add me to your private repo in your space (`hathawayj`)
3. Build your app and Docker container
4. Update your `readme.md` with details about your app and how to start it.
5. Include a screen shot of your working app in your repository.
6. Submit the link to your repo to me in Canvas within your vocabulary/lingo challenge.

## Vocabulary/Lingo Challenge

_Within a `.md` file in your repository and as a submitted `.pdf` or `.html` on Canvas, address the following items;_

1. A link to your repo that you have shared with me and a screenshot of your app.
2. Explain the added value of using DataBricks in your Data Science process (using text, diagrams, or tables).
3. Compare and contrast PySpark to either Pandas or the Tidyverse (using text, diagrams, or tables).
4. Explain Docker to somebody intelligent but not a tech person (using text, diagrams, or tables).

Your answers should be clear, detailed, and no longer than is needed. Imagine you are responding to a client or as an interview candidate._

- _Clear:_ Clean sentences in nicely laid out format.
- _Detailed:_ You touch on all the critical points of the concept. Speak at a reasonable level.
- _Brevity:_ Don't ramble. Get to the point, and don't repeat yourself.

## Submission

Submit your work on Canvas.  It can be a link to your repository or a PDF/HTML file with your vocabulary challenge and a link to your repo included.

## References

- [Streamlit Dashboard](https://streamlit.io/)
- [Docker](https://www.docker.com/)
- [Dockerfile cheat sheet](https://kapeli.com/cheat_sheets/Dockerfile.docset/Contents/Resources/Documents/index)
- [Streamlit deploy in Docker](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
- [Streamlit and Docker](https://maelfabien.github.io/project/Streamlit/#)
- [Using the Open Weather Map API with Python](https://knasmueller.net/using-the-open-weather-map-api-with-python)
- [OpenWeatherMap API Python](https://rapidapi.com/blog/openweathermap-api-overview/python/)
- [Wikipedia on JSON](https://en.wikipedia.org/wiki/JSON)
