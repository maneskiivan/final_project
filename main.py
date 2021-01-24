import requests
from simple_term_menu import TerminalMenu
import keyring
import pandas as pd
import csv
from os import path

class Search:
  '''Performs a search by calling the API and saves the response in a dictionary'''
  def __init__(self):
    '''initialize a search menu'''
    self.__search_input = {'offset': '0', 'limit': '5'}
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
        self.__search_input['state_code'] = input('\nEnter the state code you wish to search in: ')
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
        if not self.__submit_search():
          break
        elif self.__submit_search():
          continue
      elif menu_entry_index == 7:
        break

  def __submit_search(self):
    '''Submits a search to the API and saves the results in to a dict'''
    url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"
    headers = {
      'x-rapidapi-key': self.__api_key,
      'x-rapidapi-host': "realtor.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=self.__search_input)
    # creating a dict from the JSON response
    response_dict = response.json()
    if response_dict['properties']:
      try:
        # creating a new organized dict that can be used for saving the data to files or analyzing it as a df
        address_list = []
        baths_list = []
        beds_list = []
        price_list = []
        web_url_list = []
        type_list = []
        for property in response_dict['properties']:
          address = f"{property['address']['line']} {property['address']['city']}, {property['address']['state_code']} {property['address']['postal_code']}"
          address_list.append(address)
          baths_list.append(property['baths'])
          beds_list.append(property['beds'])
          price_list.append(property['price'])
          type_list.append(property['prop_type'])
          web_url_list.append(property['rdc_web_url'])
        self.__search_results['Address'] = address_list
        self.__search_results['Bathrooms'] = baths_list
        self.__search_results['Bedrooms'] = beds_list
        self.__search_results['Price'] = price_list
        self.__search_results['Property Type'] = type_list
        self.__search_results['Web URL'] = web_url_list
        print('\nYou have successfully submitted your search.\n')
        return 0
      except:
        print('\nOne or more of your inputs are incorrect or non existing.')
        print('Please try again.\n')
        return 1
    elif not response_dict['properties']:
      print('\nOne or more of your inputs are incorrect or non existing.')
      print('Please try again.\n')
      return 1

  def save_search(self):
    '''Saves the search to a .csv file in the saved_searches folder only if the filename doesn't exist'''
    file_name = input('Enter a name for your file: ')
    if path.exists(f'saved_searches/{file_name}.csv'):
      print('\nThere is an existing file with the same name. Please use another name.\n')
    elif not path.exists(f'saved_searches/{file_name}.csv'):
      df = pd.DataFrame(self.__search_results)
      df.to_csv(path_or_buf=f'saved_searches/{file_name}.csv', index=False, quoting=csv.QUOTE_NONE, escapechar='"')
      print('Your search was saved successfully in the saved_searches folder.')


