from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CurrentCredit = models.IntegerField(default=100)

    def create_customer_profile(sender, **kwargs):
        #if created:
         if kwargs['created']:
            #Customer.objects.create(user=instance)
            Customer.objects.create(user=kwargs['instance'].user)
    post_save.connect(create_customer_profile, sender=User)

    def __str__(self):
        return self.user.username +' - '+ self.user.email +'-' + str(self.CurrentCredit)

class Transfers(models.Model):
    SentBy = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='sender_of_credits')
    ReceivedBy = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='receiver_of_credits')
    CreditsTransfered = models.IntegerField()
    TimeStamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.SentBy.user.username)+' sent '+str(self.CreditsTransfered)+' to '+str(self.ReceivedBy.user.username)
