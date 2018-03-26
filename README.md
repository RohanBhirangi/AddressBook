# Address Book

This is a RESTful API for an address book with an Elasticsearch data store.


## Data Model
The data model of a contact is defined as follows:-
<br>{
<br>"name": "John",
<br>"number": "1234567890",
<br>"address": "123 Maple Ave, Orange, AB",
<br>"email": "john@xyz.com"
<br>}

The input values should satisfy the following constraints:-
<br>**name**: Contact name can contain alphanumeric characters without spaces. It cannot have more than 20 characters. It should be unique; no two contacts can have the same name.
<br>**number**: Contact number can contain only digits (no '+' or '-' signs). It can have a maximum of 15 digits.
<br>**address**: Contact address can have alphanumeric characters not more than 140.
<br>**email**: Contact email needs to be of the form abc@xyz.pqr. It cannot have more than 80 characters.

## API Endpoints
* **GET** /contact?pageSize={}&page={}&query={}
<br>Fetches all the contacts in the data store. pageSize defines the number of results to be returned (default = 10000). page defines the offset from the first result you want to fetch (default = 0). query parameter can be used to query a word in any of the fields, for e.g. 'John' in name or 'Orange' in address. If no query parameters is specified, all contacts are fetched. All the parameters are optional. It returns a list of the fetched contacts or an empty list if no contacts are fetched.

* **POST** /contact
<br>Creates a new contact in the data store. Contact information can be relayed in the POST data viz., 'name', 'number', address' and 'email'. All fields are **required** in the POST data. If the contact is created successfully, a true acknowledgement is returned else a false acknowledgement with an error message is returned.

* **GET** /contact/{name}
<br>Fetches a single contact based on the name provided in the endpoint. If the contact is not present, it returns an empty list.

* **PUT** /contact/{name}
<br>Updates a contact based on the name provided in the endpoint. Contact information can be relayed in the POST data viz., 'name', 'number', address' and 'email'. All fields are **required** in the POST data (even if they are not to be changed in the existing contact). If the contact is updated successfully, a true acknowledgement is returned else a false acknowledgement with an error message is returned.

* **DELETE** /contact/{name}
<br>Deletes the contact based on the name provided in the endpoint. If the contact is deleted successfully, a true acknowledgement is returned else a false acknowledgement with an error message is returned.

## Running the API server
* Make sure you are at the root folder (contains addressbook, api, datastore, test, config.py, manage.py etc.).
* It is better to activate the virtual environment as the project requires some additional packages such as validate_email. You would need 'virtualenv' for this.
```
pip install virtualenv
```
* To activate the virtual environment, enter the following command.
```
source venv/bin/activate
```
* To run the server, enter the following command.
```
python manage.py runserver
```
* The root folder contains a config.py file which can be used to configure the host and port of the Elasticsearch data store.
```
elasticsearch_host = "http://localhost"
elasticsearch_port = "9200"
```

## Running the Unit Tests
* Make sure you are at the root folder.
```
python test/test_elasticsearch.py -v
```
Running the unit tests will delete the elasticsearch index and any data that might have been populated.

## Code Structure
* root
	* addressbook: The main project folder
		* settings.py: Specifies various settings related to the project
		* urls.py: Defines endpoints URL mapping scheme for 'addressbook'
	* api: 'api' application of the main 'addressbook' project
		* urls.py: Defines URL mapping scheme for 'api'
		* views.py: Handles http requests made over the endpoints
	* datastore: Contains data store handlers
		* elasticsearch_handler.py: Contains elasticsearch storage/retrieval logic
		* validity_handler.py: Contains input field validity checking logic
	* test: Contains unit tests for the data store handlers
		* test_elasticsearch.py: Contains unit tests for elasticsearch logic
	* venv: The virtual environment of the project
	* config.py: Contains configurable properties such as elasticsearch host and port

###### Assumptions
* Contact name should be a single word i.e., it should not contain any spaces. This is because we are specifying the name in some of our API endpoints. If names with spaces are allowed, like 'John Doe' and 'John Walker', then the /contact/John endpoint would not be able to distinguish which contact to access. This is why the contact names are unique and do not contain spaces.
* The fields for the POST and PUT queries are passed through POST data (or body) and not through query parameters.
* All fields required for the POST AND PUT endpoints even if they are the same as the existing contact.

###### Technical Specifications
* Django==2.0.3
* elasticsearch==6.2.0
* validate-email==1.3