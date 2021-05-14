# UCI Webreg API
> A public API that serves information about courses currently being offered at UCI

## Table of Contents
1. [Usage](#Usage)
    1. [Routes](#Routes)
    2. [Limitations](#limitations)
2. [Development](#development)
    1. [Install Dependencies](#development)
    2. [Run the Scraper](#development)
    3. [Run the API](#development)
3. [Contributing](#contributing)

## Usage
> The API is deployed on Heroku at https://uci-webreg-api.herokuapp.com

### Routes
  - GET `/api/course/:id/:year/:quarter`
  - Example: `/api/course/34000/2021/fall`
    - Returns the course by the given `id`, `year`, and `quarter`
  - GET `/api/dept/:dept/:year/:quarter`
  - Example: `/api/dept/COMPSCI/2021/fall`
    - Returns all courses by the given `dept`, `year`, and `quarter`

### Limitations
  - The API currently only supports requests for courses being offered in the upcoming Fall, 2021 Quarter.

## Development
1. Install Dependencies
    - Easy mode (might clash with current depends)
        ```sh
        pip install -r requirements.txt
        ```
    - Prefered Method (venv)
        ```sh
        python3 -m venv venv
      
        source venv/bin/activate
    
        pip install -r requirements.txt
        ```

2. Run the Scraper
    - From root directory 
        ```sh
        python webreg_api/scraper_wrapper.py
        ```

3. Run the API
    - From root directory
        ```sh
        python webreg_api/api.py
        ```

## Contributing
1. Fork it (<https://github.com/tarandeept/webreg-api>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
