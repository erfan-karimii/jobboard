from time import sleep
from datetime import datetime
from django.db.models import Count
from django.conf import settings
from celery import shared_task

from account.models import CompanyProfile
from job.models import Job

from .pdf_generator import PDF

@shared_task
def company_analytics(company_profile_id): # FIXME: make this function clean
    company_profile = CompanyProfile.objects.get(id=company_profile_id)
    jobs = Job.objects.filter(company=company_profile,status=True)
    jobs_per_category = jobs.values('category__name').annotate(count_job=Count('id'))
    

    pdf = PDF()
    pdf.set_title(f'analytics')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(1000, 10, f'Hello dear {company_profile.name}!')
    pdf.ln()
    pdf.set_font('Arial',style="I",size=13)
    pdf.cell(40, 10, f'Here are your analytics:')
    pdf.ln()
    pdf.set_font('Arial',style="")
    pdf.cell(40, 10, f'your available jobs: {jobs.count()}')
    pdf.ln()
    for job in jobs_per_category:
        pdf.cell(40, 10, f'{job["category__name"]}: {job["count_job"]}')
        pdf.ln()
    
    # TODO: add 10 top job with most apply 

    pdf_name = str(company_profile.name).replace(' ','-') + '|' + str(datetime.now().date())
    pdf.output(f'{settings.MEDIA_ROOT}/{pdf_name}.pdf')

    return company_profile.name