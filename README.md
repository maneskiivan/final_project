# FINAL PROJECT
## MY REALTOR

### Introduction

The My Realtor app helps you perform searches for realestate properties that are posted for sale. You can do custom searches based on different conditions like location, price and other. You can save your searches. The app can do analysis from the response data or from the saved searches.

### API

The My Realtor app is leveraging the following API to obtain the data for the searches:

[Realotr API](https://rapidapi.com/apidojo/api/realtor/endpoints)

### Installation

These instructions are for macOS devices only. Create a folder for your app and name it. Create a subfolder named 'saved_searches'. Open terminal and access the parent folder.

Run the following command to create virtual enviorement: python3 -m venv env

In the same folder run the following command so you can activate the virtual enviorement: source env/bin/activate

Run the following commands to install the necessary libraries:

pip3 install requests

pip3 install simple-term-menu

pip3 install keyring

pip3 install pandas

pip install tabulate

### Classes

Search()

AnylyzeSearch(Search)

MainMenu()
