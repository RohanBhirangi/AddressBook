from elasticsearch import Elasticsearch
import config
from datastore import validity_handler

# Retrieve host and port from config file
host = config.elasticsearch_host
port = config.elasticsearch_port

# Connect to elasticsearch on the specified host and port
es = Elasticsearch(host + ":" + port + "/")

# Create an index named 'addressbook'
es.indices.create(index='addressbook', ignore=400)
id_number = 0


def insert_contact(data):
    if not es.indices.exists(index='addressbook'):
        es.indices.create(index='addressbook', ignore=400)

    global id_number
    id_number += 1

    response = {}

    # Check if contact name already exists
    if contact_exists(data["name"]):
        response["acknowledged"] = False
        response["message"] = "Contact name already exists."
        return response

    # Check if contact name is valid
    if not validity_handler.check_name(data["name"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact name conforms to the required specifications."
        return response

    # Check if contact number is valid
    if not validity_handler.check_number(data["number"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact number conforms to the required specifications."
        return response

    # Check if contact address is valid
    if not validity_handler.check_address(data["address"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact address conforms to the required specifications."
        return response

    # Check if contact email is valid
    if not validity_handler.check_email(data["email"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact email is valid."
        return response

    es.index(index="addressbook", doc_type="contact", id=id_number, body=data)
    response["acknowledged"] = True
    return response


def get_contacts(page_size, page, query):
    if not es.indices.exists(index='addressbook'):
        es.indices.create(index='addressbook', ignore=400)

    if page_size is None:
        page_size = 5000
    if page is None:
        page = 0

    # If query is not specified, fetch all the contacts
    if query is None:
        results = es.search(index="addressbook", doc_type="contact", body={"query": {"match_all": {}}}, size=page_size,
                            from_=page)

    # If query is specified, match the query with all the fields
    else:
        results = es.search(index="addressbook", doc_type="contact",
                            body={"query": {"multi_match": {"query": query, "fields": ["name", "number", "address"]}}},
                            size=page_size, from_=page)
    return results["hits"]["hits"]


def get_contact(query):
    if not es.indices.exists(index='addressbook'):
        es.indices.create(index='addressbook', ignore=400)

    results = es.search(index="addressbook", doc_type="contact", body={"query": {"match": {"name": query}}})
    return results["hits"]["hits"]


def update_contact(query, data):
    if not es.indices.exists(index='addressbook'):
        es.indices.create(index='addressbook', ignore=400)

    response = {}

    # Check if the contact to be updated exists
    if not contact_exists(query):
        response["acknowledged"] = False
        response["message"] = "Contact does not exist."
        return response

    # Check if user wants to update the name of the contact
    # If yes, check if the new contact name does not already exist
    if query.lower() != data["name"] and contact_exists(data["name"]):
        response["acknowledged"] = False
        response["message"] = "Contact name already exists."
        return response

    # Check if contact name is valid
    if not validity_handler.check_name(data["name"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact name conforms to the required specifications."
        return response

    # Check if contact number is valid
    if not validity_handler.check_number(data["number"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact number conforms to the required specifications."
        return response

    # Check if contact address is valid
    if not validity_handler.check_address(data["address"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact address conforms to the required specifications."
        return response

    # Check if contact email is valid
    if not validity_handler.check_email(data["email"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact email is valid."
        return response

    # Retrieve the id of the contact to be updated
    results = es.search(index="addressbook", doc_type="contact", body={"query": {"match": {"name": query}}})
    update_id = results["hits"]["hits"][0]["_id"]

    # Update the contact corresponding to the retrieve id
    es.index(index="addressbook", doc_type="contact", id=update_id, body=data)
    response["acknowledged"] = True
    return response


def delete_contact(query):
    if not es.indices.exists(index='addressbook'):
        es.indices.create(index='addressbook', ignore=400)

    response = {}

    results = es.search(index="addressbook", doc_type="contact", body={"query": {"match": {"name": query}}})

    # Check if the contact to be deleted exists
    if len(results["hits"]["hits"]) == 0:
        response["acknowledged"] = False
        response["message"] = "Contact does not exist."
        return response

    # Retrieve the id of the contact to be deleted
    delete_id = results["hits"]["hits"][0]["_id"]

    # Delete the contact corresponding to the retrieve id
    es.delete(index="addressbook", doc_type="contact", id=delete_id)
    response["acknowledged"] = True
    return response


def contact_exists(name):
    if not es.indices.exists(index='addressbook'):
        es.indices.create(index='addressbook', ignore=400)

    results = es.search(index="addressbook", doc_type="contact", body={"query": {"match": {"name": name}}})
    if len(results["hits"]["hits"]) > 0:
        return True
    return False
