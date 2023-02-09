from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from scanner.models import Website, Subdomain
from scanner.serializers import ScanSerializer


class Scan(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Website.objects.all()
    serializer_class = ScanSerializer


class Result(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        website = Website.objects.get(id=id)
        subdomain_results = [{subdomain.subdomain_name: subdomain.result, "ip": subdomain.ip_address} for subdomain in Subdomain.objects.filter(website=website).all()]
        return Response({"date": website.created_at, "subdomains": subdomain_results})
