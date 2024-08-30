from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import CompanyProfile,UserProfile
from django.core.exceptions import ValidationError

class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Job(models.Model):
    PROVINCE_CHOICES = (
        ("AL", _("Alborz")),
        ("AR", _("Ardabil")),
        ("AE", _("Azerbaijan East")),
        ("AW", _("Azerbaijan Wast")),
        ("BU", _("Bushehr")),
        ("CM", _("Chahar Mahaal and Bakhtiari")),
        ("FA", _("Fars")),
        ("GI", _("Gilan")),
        ("GO", _("Golestan")),
        ("HA", _("Hamadan")),
        ("HO", _("Hormozgan")),
        ("IL", _("Ilam")),
        ("IS", _("Isfahan")),
        ("KE", _("Kerman")),
        ("KM", _("Kermanshah")),
        ("KN", _("Khorasan North")),
        ("KR", _("Khorasan Razavi")),
        ("KS", _("Khorasan South")),
        ("KH", _("Khuzestan")),
        ("KB", _("Kohgiluyeh and Boyer-Ahmad")),
        ("KU", _("Kurdistan")),
        ("LO", _("Lorestan")),
        ("MA", _("Markazi")),
        ("MZ", _("Mazandaran")),
        ("QA", _("Qazvin")),
        ("QO", _("Qom")),
        ("SE", _("Semnan")),
        ("SB", _("Sistan and Baluchestan")),
        ("TH", _("Tehran")),
        ("YZ", _("Yazd")),
        ("ZN", _("Zanjan")),
    )
    
    company = models.ForeignKey(CompanyProfile,on_delete=models.CASCADE,editable=False)
    title = models.CharField(max_length=400)
    category = models.ForeignKey(JobCategory,on_delete=models.SET_NULL,null=True)
    province = models.CharField(max_length=50,choices=PROVINCE_CHOICES)
    salary = models.IntegerField()
    info = models.TextField()

    status = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " " + self.company.user.email + " " + str(self.status)


def validate_resume_size(value):
    filesize= value.size
    
    if filesize > 3485760:
        raise ValidationError("You cannot upload file more than 3MB")
    else:
        return value



class JobApply(models.Model):
    job_seeker = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE,null=True)
    cv_file = models.FileField(validators=[validate_resume_size])
    created = models.DateTimeField(auto_now_add=True)

    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.job_seeker.user.email} to {self.job.company.name} for {self.job.title}"