# Streamlit made web-app development a breeze

This project demonstrates the ease of web-app development through Streamlit. To illustrate this ease of web-app development with Streamlit for data sharing, we use Coronavirus live data from worldometers.info. With just a couple of lines of codes, one can readily create interactive widgets, present a table of data and interactive charts.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

And environment with Streamlit library installed. Due to its tied dependencies on a number of libraries, it is recommended to use a Python virtual environment (virtualenv) and Streamlit installed there.

```
On Mac, create a virtual environment called venv with pip and python:
$ conda create -n venv pip python=3.6
To activate this environment, use:
> source activate venv
To install Streamlit, use:
> pip install streamlit

On Linux, each step above could be done as follows, respectively:
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
$ pip install streamlit
```

### Running

A step by step series of examples that tell you how to get a development env running

```
To start the web-app from your dev machine:
> streamlit run covid_app.py

To start it without downloading to your local machine, use:
> streamlit run https://raw.githubusercontent.com/drskennedy/streamlit_covid/master/covid_app.py
```

## Built With

* [Streamlit](https://www.streamlit.io/)

## Authors

* **Kennedy Selvadurai**

## License

This project is licensed under the GNU General Public License - see the [LICENSE.md](LICENSE.md) file for details
