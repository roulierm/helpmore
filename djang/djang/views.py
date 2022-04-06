from re import sub
from django.shortcuts import render
from requests import get
from . import donation_amount_calc, cookies, fiftyone_api

from .forms import DonationForm, MyCustomForm


def writedono(list):
    MyFile=open('dono.txt','w')

    for element in list:
        MyFile.write(str(element))
        MyFile.write('\n')
    MyFile.close()

def index(request):

    cookies.main(request)

    userinfo = fiftyone_api.main(request)

    print(userinfo)

    lastdono = cookies.getcookie(request)
    ip = get('https://api.ipify.org').text
    recdono = donation_amount_calc.main(ip, lastdono)
    print(recdono)

    list_of_tuples=[    
    ('0', str(recdono[0])),
    ('1', str(recdono[1])),
    ('2', str(recdono[2])),
    ('3', str(recdono[3])),
    ('4', str(recdono[4])),
    ]
    
    form = MyCustomForm(my_choices=list_of_tuples)

    context = {"recdono": recdono, "form": form}
    response = render(request, 'djang/index.html', context)

    submitteddono = 0
    print("SUMBITTED DONO " + str(submitteddono))
    cookies.setcookie(response, submitteddono)

    tip = int(submitteddono * .15)
    link = "https://link.justgiving.com/v1/charity/donate/charityId/13441?donationValue="+str(submitteddono)+"&totalAmount="+str(submitteddono+tip)+"&currency=GBP&skipGiftAid=true&skipMessage=true"

    print(link)
    print("post request")
    print(request.POST.get("myselectedbtn"))
    return response