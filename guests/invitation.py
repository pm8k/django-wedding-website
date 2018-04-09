from email.mime.image import MIMEImage
import os
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template.loader import render_to_string
from guests.models import Party, MEALS
from django.http import HttpResponseRedirect, HttpResponse


INVITATION_TEMPLATE = 'guests/email_templates/invitation.html'


def guess_party_by_invite_id_or_404(request,invite_id):
    try:
        return True, Party.objects.get(invitation_id=invite_id)
    except Party.DoesNotExist:
        # if settings.DEBUG:
        #     # in debug mode allow access by ID
        #     #return Party.objects.get(id=int(invite_id))
        # else:
        #     raise Http404()
        return False, HttpResponseRedirect('/invite/{invite_id}/'.format(invite_id=request.user.username))
