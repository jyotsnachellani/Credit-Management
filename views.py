from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Customer, Transfers

def Home(request):

    return render(request,'Home.html')
# Create your views here.
def Users(request):
    customers = Customer.objects.all().order_by('id')
    return render(request, "Users.html", {'customers': customers})

def ViewUser(request, id):
    id = id
    try:
        userinfo = Customer.objects.get(pk=id)
        customers = Customer.objects.all()
        return render(request, "ViewUser.html", {'userinfo': userinfo, 'customers': customers})
    except:
        return HttpResponse("<h1>User does not exist</h1>")

def TransferView(request):
    transfers = Transfers.objects.all().order_by('-id')
    return render(request, "Transfers.html", {'transfers':transfers})

def CreditTransfer(request, id):
    if request.method == "POST":
        Credits = int(request.POST['Credits'])
        ReceiverId = request.POST.get('ReceiverId')
        sender = Customer.objects.get(pk=id)
        senderCredits = int(sender.CurrentCredit)-Credits
        if senderCredits < 0:
            messages.error(request, "Insufficent Credits")
            return redirect('/ViewUser/'+str(id))
        elif Credits < 0:
            messages.error(request, "Enter Positive Credits")
            return redirect('/ViewUser/' + str(id))
        else:
            receiver = Customer.objects.get(pk=ReceiverId)
            receiver.CurrentCredit = int(receiver.CurrentCredit) + Credits
            receiver.save()
            sender.CurrentCredit = int(sender.CurrentCredit) - Credits
            sender.save()
            Transfers.objects.create(SentBy=sender, ReceivedBy=receiver, CreditsTransfered=Credits)
            messages.success(request, "Credits Transferred Successfully.")
            return redirect('/ViewUser/' + str(id))