from collections import OrderedDict

from django.shortcuts import render

from test_app.models import Account


def index(request):

    data = OrderedDict()
    for account in Account.objects.all():
        data[account] = account.user_set.all()

    return render(request, 'index.html', context={'users': data, 'this_user': request.user})
