from elasticsearch import Elasticsearch
import config
from datastore import validity_handler

host = config.elasticsearch_host
port = config.elasticsearch_port

es = Elasticsearch(host + ":" + port + "/")
es.indices.create(index='addressbook', ignore=400)
id_number = 0


def insert_contact(data):
    if not es.indices.exists(index='addressbook'):
        es.indices.create(index='addressbook', ignore=400)

    global id_number
    response = {}
    id_number += 1

    if contact_exists(data["name"]):
        response["acknowledged"] = False
        response["message"] = "Contact name already exists."
        return response

    if not validity_handler.check_name(data["name"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact name conforms to the required specifications."
        return response

    if not validity_handler.check_number(data["number"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact number conforms to the required specifications."
        return response

    if not validity_handler.check_address(data["address"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact address conforms to the required specifications."
        return response

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
    if query is None:
        results = es.search(index="addressbook", doc_type="contact", body={"query": {"match_all": {}}}, size=page_size,
                            from_=page)
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

    if not contact_exists(query):
        response["acknowledged"] = False
        response["message"] = "Contact does not exist."
        return response

    if query.lower() != data["name"] and contact_exists(data["name"]):
        response["acknowledged"] = False
        response["message"] = "Contact name already exists."
        return response

    if not validity_handler.check_name(data["name"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact name conforms to the required specifications."
        return response

    if not validity_handler.check_number(data["number"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact number conforms to the required specifications."
        return response

    if not validity_handler.check_address(data["address"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact address conforms to the required specifications."
        return response

    if not validity_handler.check_email(data["email"]):
        response["acknowledged"] = False
        response["message"] = "Please check if contact email is valid."
        return response

    results = es.search(index="addressbook", doc_type="contact", body={"query": {"match": {"name": query}}})
    update_id = results["hits"]["hits"][0]["_id"]
    es.index(index="addressbook", doc_type="contact", id=update_id, body=data)
    response["acknowledged"] = True
    return response


def delete_contact(query):
    if not es.indices.exists(index='addressbook'):
        es.indices.create(index='addressbook', ignore=400)

    response = {}
    results = es.search(index="addressbook", doc_type="contact", body={"query": {"match": {"name": query}}})
    if len(results["hits"]["hits"]) == 0:
        response["acknowledged"] = False
        response["message"] = "Contact does not exist."
        return response
    delete_id = results["hits"]["hits"][0]["_id"]
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
