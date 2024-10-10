import concurrent.futures
import requests
import time
import random
import string

# List of URLs to hit
urls = [
    #queries
    'https://fleetpanda.metabaseapp.com/api/public/card/8d83d1f5-f6e2-4d40-8426-4fd1dbbef833/query?parameters=%5B%7B%22type%22%3A%22date%2Fsingle%22%2C%22value%22%3Anull%2C%22id%22%3A%223efef146-68b9-46f9-98e7-63faea61af30%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22date_start%22%5D%5D%7D%2C%7B%22type%22%3A%22date%2Fsingle%22%2C%22value%22%3Anull%2C%22id%22%3A%2215906cae-e52d-4729-90c1-1eb41bbf0843%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22date_end%22%5D%5D%7D%2C%7B%22type%22%3A%22category%22%2C%22value%22%3Anull%2C%22id%22%3A%221a9a0c07-91cf-4a6b-a8bb-2735a548dfb5%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22product%22%5D%5D%7D%2C%7B%22type%22%3A%22number%2F%3D%22%2C%22value%22%3Anull%2C%22id%22%3A%22675028ca-56fb-42a5-9e2d-54f6a2514925%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22shifts%22%5D%5D%7D%2C%7B%22type%22%3A%22number%2F%3D%22%2C%22value%22%3Anull%2C%22id%22%3A%2293b9232a-2508-4be4-a015-2c4be4977b89%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22order_groups%22%5D%5D%7D%5D',
    'https://fleetpanda.metabaseapp.com/api/public/card/85537187-8cbd-43e3-b49e-d1e3994e1c69/query?parameters=%5B%7B%22type%22%3A%22date%2Fall-options%22%2C%22value%22%3A%22past30days%22%2C%22id%22%3A%226ac281cc-a462-6d74-798e-19f90857fb6e%22%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22date%22%5D%5D%7D%2C%7B%22type%22%3A%22string%2Fcontains%22%2C%22value%22%3Anull%2C%22id%22%3A%22a4a65c59-975b-7846-2b4e-3dd567e1bfb9%22%2C%22options%22%3A%7B%22case-sensitive%22%3Afalse%7D%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22customer_id%22%5D%5D%7D%2C%7B%22type%22%3A%22string%2Fcontains%22%2C%22value%22%3Anull%2C%22id%22%3A%225e706825-341a-c437-edb8-87b5f8738d9e%22%2C%22options%22%3A%7B%22case-sensitive%22%3Afalse%7D%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22shipto_id%22%5D%5D%7D%2C%7B%22type%22%3A%22string%2Fcontains%22%2C%22value%22%3Anull%2C%22id%22%3A%22cab93432-8231-0ac3-56e2-08f01bb35c21%22%2C%22options%22%3A%7B%22case-sensitive%22%3Afalse%7D%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22driver_id%22%5D%5D%7D%2C%7B%22type%22%3A%22number%2F%3D%22%2C%22value%22%3A%5B%22100%22%5D%2C%22id%22%3A%2214bc8a24-1223-963e-7979-1db57f5070aa%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22limit%22%5D%5D%7D%5D',
    'https://fleetpanda.metabaseapp.com/api/public/card/4b1d2df7-2305-4a6a-a822-78867f90700b/query?parameters=%5B%7B%22type%22%3A%22date%2Fall-options%22%2C%22value%22%3A%22past30days%22%2C%22id%22%3A%225d4be69a-831f-b696-7320-af08fa356ab4%22%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22date%22%5D%5D%7D%2C%7B%22type%22%3A%22string%2Fcontains%22%2C%22value%22%3Anull%2C%22id%22%3A%2299a0ec40-52d9-9c0c-37a5-3df77b19c1af%22%2C%22options%22%3A%7B%22case-sensitive%22%3Afalse%7D%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22customer_id%22%5D%5D%7D%2C%7B%22type%22%3A%22string%2Fcontains%22%2C%22value%22%3Anull%2C%22id%22%3A%22d3aea141-50d6-f1a7-78b5-5f0ef0ea9db7%22%2C%22options%22%3A%7B%22case-sensitive%22%3Afalse%7D%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22shipto_id%22%5D%5D%7D%2C%7B%22type%22%3A%22string%2Fcontains%22%2C%22value%22%3Anull%2C%22id%22%3A%2292e86c11-c96a-24c2-277b-2144adb31fca%22%2C%22options%22%3A%7B%22case-sensitive%22%3Afalse%7D%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22driver_id%22%5D%5D%7D%2C%7B%22type%22%3A%22number%2F%3D%22%2C%22value%22%3A%5B100%5D%2C%22id%22%3A%22f194b08a-ceac-06eb-6b81-3ca76a2fb232%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22limit%22%5D%5D%7D%5D',
    'https://fleetpanda.metabaseapp.com/api/public/card/1535b33d-570c-468e-8ab6-e1fc657da913/query?parameters=%5B%7B%22type%22%3A%22date%2Fsingle%22%2C%22value%22%3Anull%2C%22id%22%3A%22428c453d-cc76-4f1e-a4a5-e6a7be9e7566%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22date_start%22%5D%5D%7D%2C%7B%22type%22%3A%22date%2Fsingle%22%2C%22value%22%3A%222024-09-16%22%2C%22id%22%3A%2283cbe1d3-c7c0-4cd2-abc8-4c55cb624dde%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22date_end%22%5D%5D%7D%2C%7B%22type%22%3A%22category%22%2C%22value%22%3Anull%2C%22id%22%3A%226b3684e8-8011-42f3-8d05-7c87b35b0da2%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22hub%22%5D%5D%7D%2C%7B%22type%22%3A%22category%22%2C%22value%22%3Anull%2C%22id%22%3A%22f0e2ac43-6a92-44bb-8065-bd690bb1469c%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22product%22%5D%5D%7D%2C%7B%22type%22%3A%22category%22%2C%22value%22%3Anull%2C%22id%22%3A%227353de88-db05-4310-8b01-d60e8b3abd13%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22customer%22%5D%5D%7D%2C%7B%22type%22%3A%22number%2F%3D%22%2C%22value%22%3Anull%2C%22id%22%3A%2219d36899-fe46-490a-b401-c83d156e79d0%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22order_groups%22%5D%5D%7D%2C%7B%22type%22%3A%22number%2F%3D%22%2C%22value%22%3Anull%2C%22id%22%3A%223eee068c-67c7-40b4-912b-c53d86fa890e%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22shifts%22%5D%5D%7D%5D',
    'https://fleetpanda.metabaseapp.com/api/public/card/5fda38ae-b29d-476b-9d18-ded4f1df283c/query?parameters=%5B%7B%22type%22%3A%22date%2Fsingle%22%2C%22value%22%3Anull%2C%22id%22%3A%22428c453d-cc76-4f1e-a4a5-e6a7be9e7566%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22date_start%22%5D%5D%7D%2C%7B%22type%22%3A%22date%2Fsingle%22%2C%22value%22%3A%222024-09-12%22%2C%22id%22%3A%2283cbe1d3-c7c0-4cd2-abc8-4c55cb624dde%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22date_end%22%5D%5D%7D%2C%7B%22type%22%3A%22category%22%2C%22value%22%3Anull%2C%22id%22%3A%226b3684e8-8011-42f3-8d05-7c87b35b0da2%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22hub%22%5D%5D%7D%2C%7B%22type%22%3A%22category%22%2C%22value%22%3Anull%2C%22id%22%3A%22f0e2ac43-6a92-44bb-8065-bd690bb1469c%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22product%22%5D%5D%7D%2C%7B%22type%22%3A%22category%22%2C%22value%22%3Anull%2C%22id%22%3A%227353de88-db05-4310-8b01-d60e8b3abd13%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22customer%22%5D%5D%7D%2C%7B%22type%22%3A%22number%2F%3D%22%2C%22value%22%3Anull%2C%22id%22%3A%2219d36899-fe46-490a-b401-c83d156e79d0%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22order_groups%22%5D%5D%7D%2C%7B%22type%22%3A%22number%2F%3D%22%2C%22value%22%3Anull%2C%22id%22%3A%223eee068c-67c7-40b4-912b-c53d86fa890e%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22shifts%22%5D%5D%7D%2C%7B%22type%22%3A%22category%22%2C%22value%22%3Anull%2C%22id%22%3A%2250922424-5e51-44ff-91c4-79ce11791f58%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22template-tag%22%2C%22ship_to%22%5D%5D%7D%5D',

    'https://fleetpanda.metabaseapp.com/api/public/card/014290f0-40f3-4a4d-8342-6b1e6121dd06/query?parameters=%5B%5D',
    'https://fleetpanda.metabaseapp.com/api/public/card/b10fba7f-9b38-4672-81fa-1bbc64c312fc/query?parameters=%5B%7B%22type%22%3A%22date%2Fall-options%22%2C%22value%22%3A%22thisday%22%2C%22id%22%3A%22fd6823f4-af8e-1ce3-7ff9-0c9b42dd4e82%22%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22date%22%5D%5D%7D%5D',
    'https://fleetpanda.metabaseapp.com/public/question/b10fba7f-9b38-4672-81fa-1bbc64c312fc?date=thisday',
    'https://fleetpanda.metabaseapp.com/public/question/014290f0-40f3-4a4d-8342-6b1e6121dd06'

   
    #urls 
     'https://fleetpanda.metabaseapp.com/public/question/8d83d1f5-f6e2-4d40-8426-4fd1dbbef833?date_start=&date_end=&product=&shifts=&order_groups=',
     'https://fleetpanda.metabaseapp.com/public/question/85537187-8cbd-43e3-b49e-d1e3994e1c69?date=past30days&customer_id=&shipto_id=&driver_id=&limit=100',
     'https://fleetpanda.metabaseapp.com/public/question/4b1d2df7-2305-4a6a-a822-78867f90700b?date=past30days&customer_id=&shipto_id=&driver_id=&limit=100',
     'https://fleetpanda.metabaseapp.com/public/question/1535b33d-570c-468e-8ab6-e1fc657da913?date_start=&date_end=2024-09-16&hub=&product=&customer=&order_groups=&shifts=',
     'https://fleetpanda.metabaseapp.com/public/question/5fda38ae-b29d-476b-9d18-ded4f1df283c?date_start=&date_end=2024-09-12&hub=&product=&customer=&order_groups=&shifts=&ship_to=',
     'https://fleetpanda.metabaseapp.com/public/question/fd08df1c-5d4d-4563-971b-a4345753fc6e?date_start=&date_end=&product=&shifts=&order_groups=',
     'https://fleetpanda.metabaseapp.com/public/question/eced53ed-6b01-4773-8f8b-6ca90f07143c?date=thisday',
     'https://fleetpanda.metabaseapp.com/public/question/557a50a4-f541-4556-ad8d-df04c3026c4c?date=past3days',
     'https://fleetpanda.metabaseapp.com/public/question/014290f0-40f3-4a4d-8342-6b1e6121dd06',
     'https://fleetpanda.metabaseapp.com/public/question/9cbb8cba-482c-4205-b5a8-4c6eab3123ea?date=past3months~&driver=',
     'https://fleetpanda.metabaseapp.com/public/question/48cb1abc-8854-4ea3-a5d1-3953705a4dc0?date=past3months~&driver=',
     'https://fleetpanda.metabaseapp.com/public/question/b10fba7f-9b38-4672-81fa-1bbc64c312fc?date=thisday',
     'https://fleetpanda.metabaseapp.com/public/question/bff0fdf5-3002-4caf-b148-89cfcf6e97eb?date=past5days',
     'https://fleetpanda.metabaseapp.com/public/question/7fd83ae0-3b68-4971-b8e1-ebea826316c3?date=&tenant=&driver='
]

# Number of users to simulate
num_users = 50  

# Time delay between requests (in seconds)
request_delay = 2 

# Function to generate a random query string to ensure unique request and bypass cache
def generate_unique_query():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"&cache_buster={random_string}"

# Function to send a request and return the response status and time
def fetch_url(url, user_id):
    start_time = time.time()  # Start timer
    
    # Append unique query parameter to the URL
    unique_url = url + generate_unique_query()
    
    # Add headers to disable cache
    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
    
    try:
        # Introduce delay before sending the request
        time.sleep(request_delay)

        response = requests.get(unique_url, headers=headers, timeout=300)  # Send the GET request
        end_time = time.time()  # End timer
        duration = end_time - start_time  # Calculate duration

        # Check if response contains data
        if response.status_code == 202 or response.status_code == 200:
            try:
                data = response.json()  # Attempt to parse JSON
                if data:
                    return f"User {user_id}, URL: {unique_url}, Status: {response.status_code}, Data Present, Response Time: {duration:.2f} seconds, Response data: {data} seconds"
                else:
                    return f"User {user_id}, URL: {unique_url}, Status: {response.status_code}, No Data Found, Response Time: {duration:.2f} seconds"
            except ValueError:
                if len(response.text.strip()) > 0:
                    return f"User {user_id}, URL: {unique_url}, Status: {response.status_code}, Data Present (Non-JSON), Response Time: {duration:.2f} seconds"
                else:
                    return f"User {user_id}, URL: {unique_url}, Status: {response.status_code}, No Data Found (Non-JSON), Response Time: {duration:.2f} seconds"
        else:
            return f"User {user_id}, URL: {unique_url}, Status Code: {response.status_code}, Error, Response Time: {duration:.2f} seconds"
    except requests.RequestException as e:
        return f"User {user_id}, URL: {unique_url}, Error: {e}"

# Function to simulate all users hitting all URLs at once
def request_all_urls_for_all_users(url_list, num_users):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_users * len(url_list)) as executor:
        futures = []
        # Simulate each user hitting all URLs
        for user_id in range(1, num_users + 1):
            for url in url_list:
                futures.append(executor.submit(fetch_url, url, user_id))  # Each user hits all URLs at once
        for future in concurrent.futures.as_completed(futures):
            try:
                print(future.result())
            except Exception as exc:
                print(f"Exception occurred: {exc}")

# Simulate all users hitting all URLs at once
request_all_urls_for_all_users(urls, num_users)
