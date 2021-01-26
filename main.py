import requests
from simple_term_menu import TerminalMenu
import keyring
import pandas as pd
import csv
from os import path, listdir
from tabulate import tabulate

class Search:
  '''Performs a search by calling the API and saves the response in a dictionary'''
  def __init__(self):
    '''initialize a search menu'''
    self.__search_input = {'offset': '0', 'limit': '200'}
    self.__search_results = {}
    # getting the api key from key chain
    self.__api_key = keyring.get_password('realtor', 'realtor')
    # Run the search menu
    print('\n\tUse the search filters to customize your search. You can use City and State in combination or just a Zip Code.')
    print('\tYou cannot use both at the same time and they are required. The last value you submit from both will take precedence.\n')
    while True:
      menu = ['1. City*', '2. State Code*', '3. Zip Code*', '4. Beds Min', '5. Bath Min', '6. Price Max', '7. Submit', '8. Exit']
      terminal_menu = TerminalMenu(menu, title='\nSearch Filters\n')
      menu_entry_index = terminal_menu.show()
      # going over the menu choices
      if menu_entry_index == 0:
        self.__search_input['city'] = input('\nEnter the name of the city you wish to search in: ')
        # if there is a zip value it gets removed from the dict
        if 'postal_code' in self.__search_input.keys():
          del self.__search_input['postal_code']
      elif menu_entry_index == 1:
        self.__search_input['state_code'] = input('\nEnter the state code you wish to search in: ').upper()
        # if there is a zip value it gets removed from the dic
        if 'postal_code' in self.__search_input.keys():
          del self.__search_input['postal_code']
      elif menu_entry_index == 2:
        self.__search_input['postal_code'] = input('\nEnter the zip code you wish to search in: ')
        # if there is city and state values they get removed form the dict
        if 'city' in self.__search_input.keys():
          del self.__search_input['city']
        if 'state_code' in self.__search_input.keys():
          del self.__search_input['state_code']
      elif menu_entry_index == 3:
        self.__search_input['beds_min'] = input('\nEnter minimum number of bedrooms: ')
      elif menu_entry_index == 4:
        self.__search_input['baths_min'] = input('\nEnter minimum number of bathrooms: ')
      elif menu_entry_index == 5:
        self.__search_input['price_max'] = input('\nEnter the maximum price: ')
      elif menu_entry_index == 6:
        if self.__submit_search():
          df = pd.DataFrame(self.__search_results)
          print(tabulate(df, headers='keys', tablefmt='psql'))
          print('\nYou have successfully submitted your search.\n')
          print('\nYou can save your last search in the main menu.')
      elif menu_entry_index == 7:
        break

  def __submit_search(self):
    '''Submits a search to the API and saves the results in to a dict'''
    url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"
    headers = {
      'x-rapidapi-key': self.__api_key,
      'x-rapidapi-host': "realtor.p.rapidapi.com"
    }
    querystring = self.__search_input

    response = requests.request("GET", url, headers=headers, params=querystring)
    # creating a dict from the JSON response
    response_dict = response.json()
    if response_dict['properties']:
      try:
        # creating a new organized dict that can be used for saving the data to files or analyzing it as a df
        street_list = []
        city_list = []
        state_list = []
        zip_code_list = []
        baths_list = []
        beds_list = []
        price_list = []
        web_url_list = []
        type_list = []
        for property in response_dict['properties']:
          street = f"{property['address']['line']}"
          street_list.append(street)
          city = f"{property['address']['city']}"
          city_list.append(city)
          state = f"{property['address']['state_code']}"
          state_list.append(state)
          zip_code = f"{property['address']['postal_code']}"
          zip_code_list.append(zip_code)
          baths_list.append(property['baths'])
          beds_list.append(property['beds'])
          price_list.append(property['price'])
          type_list.append(property['prop_type'])
          web_url_list.append(property['rdc_web_url'])
        self.__search_results['Street'] = street_list
        self.__search_results['City'] = city_list
        self.__search_results['State'] = state_list
        self.__search_results['Postal Code'] = zip_code_list
        self.__search_results['Bathrooms'] = baths_list
        self.__search_results['Bedrooms'] = beds_list
        self.__search_results['Price'] = price_list
        self.__search_results['Property Type'] = type_list
        self.__search_results['Web URL'] = web_url_list
        return True
      except:
        print('\nOne or more of your inputs are incorrect or non existing.')
        print('Please try again.\n')
        return False
    elif not response_dict['properties']:
      print('\nOne or more of your inputs are incorrect or non existing.')
      print('Please try again.\n')
      return False

  def save_search(self):
    '''Saves the search to a .csv file in the saved_searches folder only if the filename doesn't exist'''
    file_name = input('Enter a name for your file: ')
    if path.exists(f'saved_searches/{file_name}.csv'):
      print('\nThere is an existing file with the same name. Please use another name.\n')
    elif not path.exists(f'saved_searches/{file_name}.csv'):
      df = pd.DataFrame(self.__search_results)
      df.to_csv(path_or_buf=f'saved_searches/{file_name}.csv', index=False, quoting=csv.QUOTE_NONE, escapechar='"')
      print('\nYour search was saved successfully in the saved_searches folder.\n')


class AnalyzeSearch(Search):
  '''Inherits from Search, analyzes a search from a dict or saved csv search data'''
  def __init__(self):
    '''Initializes a menu'''
    while True:
      menu = ['1. Analyze a new search', '2. Analyze a saved search', '3. Exit']
      terminal_menu = TerminalMenu(menu, title='\nAnalyze Menu\n')
      menu_entry_index = terminal_menu.show()
      # going over the menu choices
      if menu_entry_index == 0:
        super().__init__()
        df = pd.DataFrame(self._Search__search_results)
        while True:
          menu = ['1. Average price', '2. Types of properties', '3. 2B/2B or more', '4. Exit']
          terminal_menu = TerminalMenu(menu, title='\nSelect the type of analysis you wish to perform\n')
          menu_entry_index = terminal_menu.show()
          # going over the menu choices
          if menu_entry_index == 0:
            print(f"\n\t\tThe average price of property in your search is: ${round(df['Price'].mean(), 2)}\n")
          elif menu_entry_index == 1:
            print(f"\n{df['Property Type'].value_counts().to_string()}\n")
          elif menu_entry_index == 2:
            mask = df['Bedrooms'] >= 2
            mask1 = df['Bathrooms'] >= 2
            print(tabulate(df[mask & mask1], headers='keys', tablefmt='psql'))
          elif menu_entry_index == 3:
            break
      elif menu_entry_index == 1:
        self.__analyze_saved()
      elif menu_entry_index == 2:
        break

  def __analyze_saved(self):
    '''Analyzes a saved search'''
    menu = []
    for file in listdir('saved_searches/'):
      menu.append(file)
    if menu:
      menu.append('Exit')
      terminal_menu = TerminalMenu(menu, title='\nSelect a file you wish to analyze\n')
      menu_entry_index = terminal_menu.show()
      for file in listdir('saved_searches/'):
        if menu_entry_index == menu.index(file):
          df = pd.read_csv(f'saved_searches/{file}')
          while True:
            menu = ['1. Average price', '2. Types of properties', '3. 2B/2B or more', '4. Exit']
            terminal_menu = TerminalMenu(menu, title='\nSelect the type of analysis you wish to perform\n')
            menu_entry_index = terminal_menu.show()
            # going over the menu choices
            if menu_entry_index == 0:
              print(f"\n\t\tThe average price of property in your search is: ${round(df['Price'].mean(), 2)}\n")
            elif menu_entry_index == 1:
              print(f"\n{df['Property Type'].value_counts().to_string()}\n")
            elif menu_entry_index == 2:
              mask = df['Bedrooms'] >= 2
              mask1 = df['Bathrooms'] >= 2
              print(tabulate(df[mask & mask1], headers='keys', tablefmt='psql'))
            elif menu_entry_index == 3:
              break
        else:
          pass
    elif not menu:
      print('\nYou have no saved searches.\n')


test = AnalyzeSearch()
