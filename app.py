from flask import Flask, render_template, request, redirect, url_for, session
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

app = Flask(__name__)
app.secret_key = 'fleetpanda'  

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    phone_number = request.form['phone_number']
    password = request.form['password']
    server_name = request.form['server_name']

    # Login API endpoint
    login_url = f"https://{server_name}.fleetpanda.com/graphql"
    
    # Send login request
    login_payload = {
        "query": f"""
        mutation SignInUser {{
            signInUser(
                input: {{ credentials: {{ phone: "{phone_number}", password: "{password}" }} }}
            ) {{
                message
                token
            }}
        }}
        """
    }
    
    response = requests.post(login_url, json=login_payload)

    if response.status_code == 200:
        # Assuming the login response contains the auth token
        data = response.json()
        token = data['data']['signInUser']['token']  # Adjust based on the actual response structure
        if token:
            session['token'] = token
            session['server_name'] = server_name
            return redirect(url_for('dashboard'))
        else:
            return 'Login failed, no token returned.', 401
    else:
        return 'Login failed, please check your credentials.', 401

@app.route('/dashboard')
def dashboard():
    if 'token' not in session:
        return redirect(url_for('index'))

    server_name = session['server_name']
    token = session['token']

    # Prepare GraphQL client
    transport = RequestsHTTPTransport(
        url=f"https://{server_name}.fleetpanda.com/graphql",
        headers={'Authorization': f'Bearer {token}'}
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Fetch schema
    query = gql('''
    {
        __schema {
            queryType { name }
            mutationType { name }
            types {
                name
                kind
                fields { name }
            }
        }
    }
    ''')
    
    schema_result = client.execute(query)

    # Parse the schema data for display
    queries = []
    mutations = []
    
    for type_info in schema_result['__schema']['types']:
        if type_info['kind'] == 'OBJECT':
            if type_info['fields'] is not None:
                if type_info['name'] == 'Query':
                    queries = [field['name'] for field in type_info['fields']]
                elif type_info['name'] == 'Mutation':
                    mutations = [field['name'] for field in type_info['fields']]

    return render_template('dashboard.html', queries=queries, mutations=mutations)

@app.route('/run-query', methods=['POST'])
def run_query():
    if 'token' not in session:
        return redirect(url_for('index'))

    server_name = session['server_name']
    token = session['token']
    graphql_query = request.form['graphql_query']
    variables = request.form['variables']

    transport = RequestsHTTPTransport(
        url=f"https://{server_name}.fleetpanda.com/graphql",
        headers={'Authorization': f'Bearer {token}'}
    )
    client = Client(transport=transport)

    query = gql(graphql_query)
    
    try:
        # Parse the variables string into a dictionary if provided
        if variables:
            variables = json.loads(variables)
        result = client.execute(query, variable_values=variables)
        return render_template('dashboard.html', queries=queries, mutations=mutations, result=result)
    except Exception as e:
        return render_template('dashboard.html', queries=queries, mutations=mutations, result=f"Error executing query: {e}")


if __name__ == '__main__':
    app.run(debug=True)
