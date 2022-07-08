from django.http import JsonResponse

from .models import Presentation

from common.json import ModelEncoder

import json

from django.views.decorators.http import require_http_methods

class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = ["title", "status"]
    def get_extra_data(self, o):
        return {
            "status": o.status.name,
            }

class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]

@require_http_methods(["POST","GET"])
def api_list_presentations(request, conference_id):
    """
    Lists the presentation titles and the link to the
    presentation for the specified conference id.

    Returns a dictionary with a single key "presentations"
    which is a list of presentation titles and URLS. Each
    entry in the list is a dictionary that contains the
    title of the presentation, the name of its status, and
    the link to the presentation's information.

    {
        "presentations": [
            {
                "title": presentation's title,
                "status": presentation's status name
                "href": URL to the presentation,
            },
            ...
        ]
    }
    """
    if request.method == "GET":
        presentations = Presentation.objects.filter(conference = conference_id)
        return JsonResponse(
            {"presentations": presentations},
            encoder=PresentationListEncoder,
        )
    else:
        content = json.loads(request.body)
        presentation = Presentation.create(conference = conference_id,**content)
        return JsonResponse(
            presentation,
            encoder= PresentationDetailEncoder,
            safe=False,
        )

    # presentations = [
    #     {
    #         "title": p.title,
    #         "status": p.status.name,
    #         "href": p.get_api_url(),
    #     }
    #     for p in Presentation.objects.filter(conference=conference_id)
    # ]
    # return JsonResponse({"presentations": presentations})

@require_http_methods(["DELETE", "PUT", "GET"])
def api_show_presentation(request, pk):
    if request.method == "GET":
        presentation = Presentation.objects.get(id=pk)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=pk).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        
        Presentation.objects.filter(id=pk).update(**content)

        presentation = Presentation.objects.get(id=pk)
        return JsonResponse(
            presentation,
            encoder= PresentationDetailEncoder,
            safe=False,
        )

