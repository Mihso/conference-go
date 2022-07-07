from django.http import JsonResponse

from .models import Conference, Location

from common.json import ModelEncoder


class LocationListEncoder(ModelEncoder):
    model = Location
    properties = ["name"]

class LocationDetailEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
        "city",
        "room_count",
        "created",
        "updated",
    ]
    def get_extra_data(self, o):
        return {"state": o.state.abbreviation}

class ConferenceDetailEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
        "description",
        "max_presentations",
        "max_attendees",
        "starts",
        "ends",
        "created",
        "updated",
        "location",
    ]
    encoders = {
        "location": LocationListEncoder(),
    }


class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = ["name"]


def api_list_conferences(request):

    conferences = Conference.objects.all()
    return JsonResponse(
        {"conferences": conferences},
        encoder=ConferenceListEncoder,
    )


def api_show_conference(request, pk):

    conference = Conference.objects.get(id=pk)
    return JsonResponse(
        conference, encoder=ConferenceDetailEncoder, safe=False
    )


def api_list_locations(request):
    """
    Lists the location names and the link to the location.

    Returns a dictionary with a single key "locations" which
    is a list of location names and URLS. Each entry in the list
    is a dictionary that contains the name of the location and
    the link to the location's information.

    {
        "locations": [
            {
                "name": location's name,
                "href": URL to the location,
            },
            ...
        ]
    }
    """
    locations = Location.objects.all()
    return JsonResponse(
        {"locations": locations},
        encoder=LocationListEncoder,
    )


def api_show_location(request, pk):
    """
    Returns the details for the Location model specified
    by the pk parameter.

    This should return a dictionary with the name, city,
    room count, created, updated, and state abbreviation.

    {
        "name": location's name,
        "city": location's city,
        "room_count": the number of rooms available,
        "created": the date/time when the record was created,
        "updated": the date/time when the record was updated,
        "state": the two-letter abbreviation for the state,
    }
    """
    location = Location.objects.get(id=pk)
    return JsonResponse(
        location, encoder=LocationDetailEncoder, safe=False,
    )
