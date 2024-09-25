import psutil
from datetime import datetime
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
    
    # TODO: add 10 top job with most apply and make this task heavier

    return company_profile.name

@shared_task
def get_server_resource_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
    log_file_path = '/var/lib/celery-log/logfile.log'  
    
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"[{timestamp}] CPU Usage: {cpu_usage}% and RAM Usage: {ram.percent}%\n")

    return True