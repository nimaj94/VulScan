import traceback

import redis
from django.core.management.base import BaseCommand
import socket

from scanner.models import Website, Subdomain


class Command(BaseCommand):
    help = 'Submit Results'

    def add_arguments(self, parser):
        parser.add_argument('website', nargs=1, type=str)

    def handle(self, *args, **options):
        website = options["website"]
        website = website[0]
        website_obj = Website.objects.get(domain=website)
        website = website.encode()
        try:
            redis_con = redis.Redis(host='localhost', port=6379, db=0)
            while redis_con.exists(website):
                result = redis_con.lpop(website)
                result = result.decode()
                subdomain_name, result = result.split('@@@@')
                try:
                    Subdomain.objects.create(subdomain_name=subdomain_name, result=result, website=website_obj,
                                             ip_address=socket.gethostbyname(subdomain_name))
                except socket.gaierror:
                    Subdomain.objects.create(subdomain_name=subdomain_name, result=result, website=website_obj)
            website_obj.status = Website.FINISHED
            website_obj.save()
        except Exception as exp:
            print(str(exp))
            print(traceback.format_exc())
            website_obj.status = Website.ERROR
            website_obj.save()

