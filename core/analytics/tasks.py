from celery import shared_task
from time import sleep
from account.models import CompanyProfile

@shared_task
def company_analytics(company_profile_id):
    sleep(5)
    company_profile = CompanyProfile.objects.get(id=company_profile_id)
    return company_profile.name