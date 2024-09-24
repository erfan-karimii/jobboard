from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.db.models import Count

import matplotlib.pyplot as plt
from fpdf import FPDF


class PDF(FPDF):
    def __init__(self,company_profile,*args,**kwargs):
        now = datetime.now()
        self.formatted_time = now.strftime("%Y-%m-%d|%H:%M:%S")
        self.company_profile = company_profile
        self.final_path = f"{settings.MEDIA_ROOT}/{str(company_profile.name).replace(' ','-')}"
        Path(f"{self.final_path}").mkdir(parents=True, exist_ok=True) # make sure destination folder exist
        
        super().__init__(*args,**kwargs)
    

    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(1000, 10, f'Hello dear {self.company_profile.name}!')
        self.ln()


    def create_body(self,body,font='Arial',style=None,size=13):
        self.set_font(font,style,size)
        self.cell(*body)
        self.ln()


    def create_category_pie_chart(self,jobs):
        jobs_per_category = jobs.values('category__name').annotate(count_job=Count('id'))
        categories = [job['category__name'] for job in jobs_per_category]
        counts = [job['count_job'] for job in jobs_per_category]

        plt.figure(figsize=(6, 6))  # Set the figure size
        plt.pie(counts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.savefig(f"{self.final_path}/{self.formatted_time}.png", format='png')
        self.image(f"{self.final_path}/{self.formatted_time}.png",)


    def generate_output(self):
        self.output(f'{self.final_path}/{self.formatted_time}.pdf')