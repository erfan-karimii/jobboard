from celery import shared_task
from core.celery import app
from account.models import CompanyProfile
from job.models import Job,JobApply
import time
from analytics.pdf_generator import PDF

@shared_task
def job_apply_pdf(comp_id,job_id):
    time.sleep(3)
    company = CompanyProfile.objects.get(id=comp_id)
    job=Job.objects.get(id=job_id,company=company)
    job_applies = JobApply.objects.filter(job=job)
    pdf = PDF(company)
    pdf.set_title('job_apply')
    pdf.add_page()
    for job_apply in job_applies:
        pdf.create_body([40, 10, f'job_seeker email: {job_apply.job_seeker.user.email} time : {job_apply.created.year}/{job_apply.created.month}/{job_apply.created.day}'],style='I')
    
    pdf.generate_output()

    return True