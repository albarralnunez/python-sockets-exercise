# Create your views here.
from .forms import UploadFileForm
from django.shortcuts import render
from socket import socket
from pub.settings import MQ_SERVER


def handle_uploaded_file(f):
    """
    Parse file and send operations.
    """
    sock = socket()
    sock.connect((MQ_SERVER['host'], MQ_SERVER['send']))
    for line in f:
        line_len = '{0:04d}'.format(len(line))
        sock.send(line_len)
        sock.send(line)
    sock.send('0001')
    sock.send('\n')
    sock.close()
    print 'file sended'


def home(request):
    if request.method == "POST":
        form_file = UploadFileForm(request.POST, request.FILES)
        if form_file.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return render(
                request,
                'accepted.html',
                {
                    'form_action': 'home'
                }
            )
    else:
        form_file = UploadFileForm()

    return render(
        request,
        'home.html',
        {
            'form_file': form_file,
            'form_action': 'home',
        }
    )
