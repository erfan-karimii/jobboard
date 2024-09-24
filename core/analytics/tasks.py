from celery import shared_task

from account.models import CompanyProfile
from job.models import Job

from .pdf_generator import PDF

@shared_task
def company_analytics(company_profile_id):
    company_profile = CompanyProfile.objects.get(id=company_profile_id)
    jobs = Job.objects.filter(company=company_profile,status=True)

    pdf = PDF(company_profile)
    pdf.set_title('analytics')
    pdf.add_page()
    
    pdf.create_body([40, 10, f'your available jobs: {jobs.count()}'],style='I')
    pdf.create_category_pie_chart(jobs)
    pdf.generate_output()
    
    # TODO: add 10 top job with most apply 

    return company_profile.name