import requests
from bs4 import BeautifulSoup


def get_url_content(url):
  """
    This function will fetch the page content by making a http(s) request and returns the page content.
  """
  url_response = requests.get(url)
  
  # Check for the response code. Status code 200 means the request was served successfully or raise an error.
  if not url_response.status_code == 200:
    raise Exception(f"Status Code: {url_response.status_code} - Failed to read data from the URL")
  return url_response.content

def parse_url_content(url_data):
  """
  Parse the page content of the URL to structure the data into Python. The page contains a table which has coordinates data and a unicode.
  This function will parse the data, create and return a list of tuples where 0th index will be x-axis, 1st will be the y-axis and and 3rd represents the unicode.
  """
  content = BeautifulSoup(url_data, "html.parser")
  table = content.find("table")

  rows = table.find_all("tr")[1:] # Slicing the list to remove the table header
  unicode_data = []
  for row in rows:
    data = row.find_all("td")
    unicode_data.append(
      (
        int(data[0].get_text().strip()),
        int(data[2].get_text().strip()),
        data[1].get_text().strip()
      )
    )
  return unicode_data
  
def generate_diplay_grid(data):
  """
  To place the data using x and y coordinates, this function will create a grid consisting of multiple lists and it will fill those lists with the blank spaces.
  We will use the maximum number of x and y axis to determine the range and then use the coordinates as the indexes to replace the space with the unicode. 
  """
  max_x = max(crd[0] for crd in data)
  max_y = max(crd[1] for crd in data)

  # Creating a grid dynamially based on coordinates
  grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

  # Filling the grid with unicode using the coordinates
  for x, y, unicode in data:
    grid[y][x] = unicode
  
  return grid



url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

content = get_url_content(url)
parsed_content = parse_url_content(content)
grid = generate_diplay_grid(parsed_content)

for row in grid:
    print("".join(row))

