from django.http import HttpResponse, QueryDict
from datastore import elasticsearch_handler
import json


# Create your views here.

def contact(request):
    if request.method == "GET":
        page_size = request.GET.get("pageSize")
        page = request.GET.get("page")
        query = request.GET.get("query")
        response = elasticsearch_handler.get_contacts(page_size, page, query)
        return HttpResponse(json.dumps(response), content_type="application/json")

    elif request.method == "POST":
        data = {}

        if request.POST.get("name") and request.POST.get("number") and request.POST.get("address") and request.POST.get(
                "email"):
            data["name"] = request.POST.get("name")
            data["number"] = request.POST.get("number")
            data["address"] = request.POST.get("address")
            data["email"] = request.POST.get("email")
            response = elasticsearch_handler.insert_contact(data)
            return HttpResponse(json.dumps(response), content_type="application/json")

        return HttpResponse(json.dumps({"acknowledged": False, "message": "Required fields not specified."}),
                            content_type="application/json")

    return HttpResponse(json.dumps({"acknowledged": False, "message": "Invalid request."}),
                        content_type="application/json")


def contact_name(request, name):
    if request.method == "GET":
        response = elasticsearch_handler.get_contact(name)
        return HttpResponse(json.dumps(response), content_type="application/json")

    elif request.method == "PUT":
        parameters = QueryDict(request.body)
        data = {}

        if parameters["name"] and parameters["number"] and parameters["address"] and parameters["email"]:
            data["name"] = parameters["name"]
            data["number"] = parameters["number"]
            data["address"] = parameters["address"]
            data["email"] = parameters["email"]
            response = elasticsearch_handler.update_contact(name, data)
            return HttpResponse(json.dumps(response), content_type="application/json")

        return HttpResponse(json.dumps({"acknowledged": False, "message": "Required fields not specified."}),
                            content_type="application/json")

    elif request.method == "DELETE":
        response = elasticsearch_handler.delete_contact(name)
        return HttpResponse(json.dumps(response), content_type="application/json")

    return HttpResponse(json.dumps({"acknowledged": False, "message": "Invalid request."}),
                        content_type="application/json")
