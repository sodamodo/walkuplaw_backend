from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


#Example view
@api_view(["GET"])
@authentication_classes([IsAuthenticated])
def get_user_charges(request):
    """
    Grab a list of formatted user charges(historical)
    :param request:
    :return:
    """
    user = request.user
    cm = CustomerManager()
    charges = cm.list_user_charges(user=user)
    return Response(status=200, data=charges)

