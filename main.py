import requests
from simple_term_menu import TerminalMenu
import keyring

class Search:
  '''Performs a search by calling the API and saves the response in a dictionary'''
  def __init__(self):
    '''initialize a search menu'''
    self.__search_input = {'offset': '0', 'limit': '200'}
    # getting the api key from key chain
    self.__api_key = keyring.get_password('realtor', 'realtor')
    # Run the search menu
    print(
      '\n\tUse the search filters to customize your search. You can use City and State in combination or just a Zip Code.\n' \
      '\tYou cannot use both at the same time and they are required. The last value you submit from both will take precedence.')
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
        self.submit_search()
      elif menu_entry_index == 7:
        break

  def submit_search(self):
    url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"
    headers = {
      'x-rapidapi-key': self.__api_key,
      'x-rapidapi-host': "realtor.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=self.__search_input)

    print(response.text)
