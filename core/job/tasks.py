from celery import shared_task
from core.celery import app
from account.models import CompanyProfile
from job.models import Job,JobApply
import time

@app.task()
def job_apply_pdf(comp_id,job_id):
    time.sleep(3)
    company = CompanyProfile.objects.get(id=comp_id)
    job=Job.objects.get(id=job_id,company=company)
    job_apply = JobApply.objects.filter(job=job)
    my_list = []
    for x in job_apply:
        my_dict = {
            "job_seeker":x.job_seeker.user.email,
            "time":f"{x.created.year}/{x.created.month}/{x.created.day}"
        }
        my_list.append(my_dict)
    print(my_list)
    return True