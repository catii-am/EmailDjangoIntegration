from django.shortcuts import render, redirect
from .forms import EmailAccountForm
from .models import EmailAccount, EmailMessage


def index(request):
    if request.method == 'POST':
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            email_account = form.save()
            return redirect('email_list', email_account_id=email_account.id)
    else:
        form = EmailAccountForm()

    email_accounts = EmailAccount.objects.all()
    return render(request, 'mails/index.html', {'form': form, 'email_accounts': email_accounts})


def email_list(request, email_account_id):
    try:
        email_account = EmailAccount.objects.get(id=email_account_id)
    except EmailAccount.DoesNotExist:
        return redirect('index')

    email_accounts = EmailAccount.objects.all()
    messages = EmailMessage.objects.filter(email_account=email_account).order_by('-received_date')
    return render(request, 'mails/email_list.html', {
        'email_account_id': email_account_id,
        'messages': messages,
        'email_accounts': email_accounts
    })
