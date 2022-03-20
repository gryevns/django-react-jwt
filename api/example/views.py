from rest_framework import decorators, response


@decorators.api_view(["GET", "POST"])
def example(request):
    return response.Response({"user": str(request.user)})
