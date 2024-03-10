# This file contains functions to interact with the Sirocco Energy API.
# The functions are used to obtain information about the available timezones, the user's projects, forecasts, backtests, and more.
# The functions are used in the Jupyter Notebook 'Sirocco Energy API - Example Usage.ipynb' to demonstrate how to use the API.

import os
from datetime import datetime, timezone
from pprint import pprint
from typing import Dict, Union

import pandas as pd
import requests

API_TOKEN = (
    os.environ.get("SIROCCO_API")
    if os.environ.get("SIROCCO_API")
    else "your_personal_token_here"
)

API_VERSION = "v1.1"

def display_json_pretty(json_data):
    """Displays JSON data in a more readable format without converting it to a string."""
    pprint(json_data)


def get_current_utc_datetime() -> str:
    """Returns the current date and time in UTC in the format '%Y/%m/%d %H:%M:%S'."""
    utc_datetime = datetime.now(timezone.utc).strftime("%Y/%m/%d %H:%M:%S")
    return utc_datetime


def get_available_timezones() -> Dict:
    """Function to get available timezones from the API"""
    url = f"https://api.sirocco.energy/national/timezones/{API_VERSION}/"
    try:
        response = requests.get(url)
        # Verifying the response status code:
        if response.status_code == 200:
            return response.json()  # Returning the JSON response if successful
        else:
            return f"Error: Received response with status code {response.status_code}"
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"  # Handling unexpected errors


def get_my_projects(return_id_project: bool = False) -> Dict:
    """Function to get projects associated with the user's personal token."""
    # validate return_id_project is a boolean
    if not isinstance(return_id_project, bool):
        raise ValueError("Error: return_id_project must be a boolean")
    url = f"https://api.sirocco.energy/national/projects/{API_VERSION}/"
    headers = {"Authorization": API_TOKEN}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            if return_id_project and response.json()["control"] == "Success":
                my_projects = response.json()
                return {p["id"]: p["name"] for p in my_projects["runs"]}
            return response.json()
        else:
            return f"Error: Received response with status code {response.status_code}"
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"


def get_forecasts_info(run, timezone="UTC") -> Dict:
    """Function to get the forecast data for an energy farm.

    Args:
        run (str): ID for your project.
        timezone (str): Timezone in which the information will be displayed. Defaults to 'UTC'.

    Returns:
        str or dict: Forecast data or error message.
    """
    url = f"https://api.sirocco.energy/national/forecast/{API_VERSION}/?run={run}&timezone={timezone}"
    headers = {
        "Authorization": API_TOKEN
    }  # Ensure API_TOKEN is defined and secured elsewhere

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Returning the JSON response if successful
        else:
            return f"Error: Received response with status code {response.status_code}"
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"


def get_selected_forecast(
    run: Union[int, str],
    timezone: str = "UTC",
    init_date: str = None,
    end_date: str = None,
) -> Dict:
    """Function to get the latest complete forecast for a specified time interval.

    Args:
        run (str): ID for your project.
        timezone (str): Timezone in which the information will be displayed. Defaults to 'UTC'.
        init_date (str): Optional. Beginning of the predictions [YYYY/MM/DD HH:mm:ss].
        end_date (str): Optional. End of the predictions [YYYY/MM/DD HH:mm:ss].

    Returns:
        str or dict: Selected forecast data or error message.
    """
    # Check run is an integer or can be converted to an integer
    try:
        int(run)
    except ValueError:
        return "Error: run must be an integer or a string that can be converted to an integer"

    # Constructing the API request URL with optional query parameters
    url = f"https://api.sirocco.energy/national/selectedforecast/{API_VERSION}/?run={run}&timezone={timezone}"
    if init_date:
        try:
            pd.to_datetime(end_date, format="%Y-%m-%d %H:%M:%S")
        except ValueError:
            return "Error: init_date must be in the format YYYY-mm-dd HH:MM:SS"
        url += f"&init={init_date}"
    if end_date:
        try:
            pd.to_datetime(end_date, format="%Y-%m-%d %H:%M:%S")
        except ValueError:
            return "Error: end_date must be in the format YYYY-mm-dd HH:MM:SS"
        url += f"&end={end_date}"

    headers = {
        "Authorization": API_TOKEN
    }  # API_TOKEN must be defined and secured elsewhere

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Successful request returns JSON data
        else:
            return f"Error: Received response with status code {response.status_code}"
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"


def get_backtests_info(
    run: Union[int, str],
    timezone: str = "UTC",
    init_date: str = None,
    end_date: str = None,
) -> Dict:
    """Function to obtain basic information for each forecast generated during the last 6 months.

    Args:
        run (str): ID for your project.
        init_date (str): Optional. Starting date of the forecast [YYYY/MM/DD HH:mm:ss].
        end_date (str): Optional. Ending date of the forecast [YYYY/MM/DD HH:mm:ss].
        timezone (str): Timezone in which the information will be displayed. Defaults to 'UTC'.

    Returns:
        str or dict: Backtests data or error message.
    """
    try:
        int(run)
    except ValueError:
        return "Error: run must be an integer or a string that can be converted to an integer"
    # Formatting the URL with the necessary query parameters
    url = f"https://api.sirocco.energy/national/backtests/{API_VERSION}/?run={run}&timezone={timezone}"
    if init_date:
        try:
            pd.to_datetime(end_date, format="%Y-%m-%d %H:%M:%S")
        except ValueError:
            return "Error: init_date must be in the format YYYY-mm-dd HH:MM:SS"
        url += f"&init={init_date}"
    if end_date:
        try:
            pd.to_datetime(end_date, format="%Y-%m-%d %H:%M:%S")
        except ValueError:
            return "Error: end_date must be in the format YYYY-mm-dd HH:MM:SS"
        url += f"&end={end_date}"

    headers = {"Authorization": API_TOKEN}  # Ensure API_TOKEN is defined securely

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Returning JSON data if successful
        else:
            return f"Error: Received response with status code {response.status_code}"
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"


def get_selected_backtests(
    run: Union[int, str],
    init_date: str = None,
    end_date: str = None,
    init_ahead: int = None,
    end_ahead: int = None,
    timezone: str = "UTC",
) -> Dict:
    """Function to obtain each forecast generated during the last 6 months.

    Args:
        run (str): ID for your project.
        init_date (str): Optional. Starting date of the forecast [YYYY-MM-DD HH:mm:ss].
        end_date (str): Optional. Ending date of the forecast [YYYY-MM-DD HH:mm:ss].
        init_ahead (str): Optional. Time from start_forecast to init [minutes].
        end_ahead (str): Optional. Time from start_forecast to end [minutes].
        timezone (str): Timezone in which the information will be displayed. Defaults to 'UTC'.

    Returns:
        str or dict: Selected backtests data or error message.
    """
    try:
        int(run)
    except ValueError:
        return "Error: run must be an integer or a string that can be converted to an integer"
    # Constructing the API request URL with necessary query parameters
    url = f"https://api.sirocco.energy/national/selectedbacktests/{API_VERSION}/?run={run}&timezone={timezone}"
    if init_date:
        try:
            pd.to_datetime(init_date, format="%Y-%m-%d %H:%M:%S")
        except ValueError:
            return "Error: init_date must be in the format YYYY-mm-dd HH:MM:SS"
        url += f"&init={init_date}"
    if end_date:
        try:
            pd.to_datetime(end_date, format="%Y-%m-%d %H:%M:%S")
        except ValueError:
            return "Error: end_date must be in the format YYYY-mm-dd HH:MM:SS"
        url += f"&end={end_date}"
    if init_ahead:
        try:
            init_ahead = int(init_ahead)
            # Ensuring init_ahead is a positive integer
            if init_ahead < 0:
                raise ValueError("Error: init_ahead must be a positive integer")
        except ValueError:
            return "Error: init_ahead must be a positive integer"
        url += f"&init_ahead={init_ahead}"
    if end_ahead:
        try:
            end_ahead = int(end_ahead)
            # Ensuring end_ahead is a positive integer
            if end_ahead < 0:
                raise ValueError("Error: end_ahead must be a positive integer")
        except ValueError:
            return "Error: end_ahead must be a positive integer"
        url += f"&end_ahead={end_ahead}"

    # check end_ahead is always greater than init_ahead, raise an error if not
    if end_ahead and init_ahead and end_ahead <= init_ahead:
        raise ValueError("Error: end_ahead must be greater than init_ahead")
    
    headers = {
        "Authorization": API_TOKEN
    }  # API_TOKEN should be defined and secured elsewhere

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Returning JSON data if successful
        else:
            return f"Error: Received response with status code {response.status_code}"
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"
