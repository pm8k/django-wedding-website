import base64
from collections import namedtuple
import random
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from guests import csv_import
from guests.invitation import guess_party_by_invite_id_or_404
from guests.models import Guest, MEALS, Party
from django.contrib.auth.decorators import user_passes_test
import logging



class GuestListView(ListView):
    model = Guest


@login_required
def export_guests(request):
    export = csv_import.export_guests()
    response = HttpResponse(export.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all-guests.csv'
    return response


@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    parties_with_pending_invites = Party.objects.filter(
        is_attending=None
    ).order_by('category', 'name')
    parties_with_unopen_invites = parties_with_pending_invites.filter(invitation_opened=None)
    parties_with_open_unresponded_invites = parties_with_pending_invites.exclude(invitation_opened=None)
    attending_guests = Guest.objects.filter(is_attending=True)
    guests_without_meals = attending_guests.filter(
        is_child=False
    ).filter(
        Q(meal__isnull=True) | Q(meal='')
    ).order_by(
        'party__category', 'first_name'
    )
    meal_breakdown = attending_guests.exclude(meal=None).values('meal').annotate(count=Count('*'))
    category_breakdown = attending_guests.values('party__category').annotate(count=Count('*'))

    print Party.objects.exclude(plus_one_is_attending=False).exclude(plus_one=False).count()
    print Guest.objects.exclude(is_attending=False).count()
    return render(request, 'guests/dashboard.html', context={
        'guests': Guest.objects.filter(is_attending=True).count()+Party.objects.filter(plus_one_is_attending=True).count(),
        'possible_guests': Guest.objects.exclude(is_attending=False).count()+Party.objects.exclude(plus_one_is_attending=False).exclude(plus_one=False).count(),
        'not_coming_guests': Guest.objects.filter(is_attending=False).count()+Party.objects.filter(plus_one_is_attending=False).count(),
        'pending_invites': parties_with_pending_invites.count(),
        'pending_guests': Guest.objects.filter(is_attending=None).count()+Party.objects.filter(is_attending=None).filter(plus_one=True).count(),
        # 'guests_without_meals': guests_without_meals,
        'parties_with_unopen_invites': parties_with_unopen_invites,
        'parties_with_open_unresponded_invites': parties_with_open_unresponded_invites,
        'unopened_invite_count': parties_with_unopen_invites.count(),
        'total_invites': Party.objects.count(),
        # 'meal_breakdown': meal_breakdown,
        'category_breakdown': category_breakdown,
        'plus_ones_attending': Party.objects.filter(plus_one_is_attending=True).count(),
        'possible_plus_ones': Party.objects.filter(plus_one=True).exclude(plus_one_is_attending=False).count(),
    })
# logger = logging.getLogger('views')

@login_required
def invitation(request, invite_id):
    # logger.error('YYZ')
    print 'INVITE TEST'
    pbool, party = guess_party_by_invite_id_or_404(request, invite_id)
    if not pbool:
        return party
    print party
    print party.name, invite_id
    if party.name != invite_id:
        print('failed')
        return HttpResponseRedirect('/rsvp/invite/{invite_id}/'.format(invite_id=invite_id))
    elif request.user.username != invite_id:
        print('wrong user')
        return HttpResponseRedirect('/rsvp/invite/{invite_id}/'.format(invite_id=request.user.username))
    if party.invitation_opened is None:
        # update if this is the first time the invitation was opened
        party.invitation_opened = datetime.utcnow()
        party.save()
    if request.method == 'POST':
        for response in _parse_invite_params(request.POST):
            print 'IN POST'
            print response
            guest = Guest.objects.get(pk=response.guest_pk)
            assert guest.party == party
            guest.is_attending = response.is_attending
            guest.meal = response.meal
            guest.diet_comments = response.diet
            print response.plus_one
            guest.save()
        if request.POST.get('comments'):
            comments = request.POST.get('comments')
            party.comments = comments if not party.comments else '{}; {}'.format(party.comments, comments)
        party.is_attending = party.any_guests_attending
        party.plus_one_is_attending = response.plus_one
        party.plus_one_diet_comments= response.plus_one_diet
        party.plus_one_meal = response.plus_one_meal
        print response.plus_one_meal
        party.save()
        return HttpResponseRedirect(reverse('rsvp-confirm', args=[invite_id]))
    print party.plus_one
    return render(request, template_name='guests/invitation.html', context={
        'party': party,
        'meals': MEALS,
    })


InviteResponse = namedtuple('InviteResponse', ['guest_pk', 'is_attending','meal', 'diet', 'plus_one',
                                                'plus_one_meal','plus_one_diet'])


def _parse_invite_params(params):
    responses = {}
    print params
    for param, value in params.items():
        if param.startswith('attending'):
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['attending'] = True if value == 'yes' else False
            responses[pk] = response
        elif param.startswith('meal'):
            print param
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['meal'] = value
            responses[pk] = response
        elif param.startswith('plus_one_meal'):
            print param
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['plus_one_meal'] = value
            responses[pk] = response
        elif param.startswith('plus_one_diet'):
            print param
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['plus_one_diet'] = value
            responses[pk] = response
        elif param.startswith('plus_one'):
            print param
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['plus_one'] = True if value == 'yes' else False
            responses[pk] = response
        elif param.startswith('diet'):
            print param
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['diet'] = value
            responses[pk] = response
    print responses
    for pk, response in responses.items():
        yield InviteResponse(pk, response['attending'],response.get('meal', None),response.get('diet', None),
         response.get('plus_one', None),response.get('plus_one_meal', None),response.get('plus_one_diet', None))

@login_required
def rsvp_redirect(request):
    print reverse('invitation',
            args=[request.user.username])
    return HttpResponseRedirect(
               reverse('invitation',
                       args=[request.user.username]))


@login_required
def rsvp_confirm(request, invite_id=None):
    print 'TEST'
    pbool, party = guess_party_by_invite_id_or_404(request, invite_id)
    if not pbool:
        return party
    if party.name != invite_id:
        print('failed')
        return HttpResponseRedirect('/rsvp/confirm/{invite_id}/'.format(invite_id=invite_id))
    elif request.user.username != invite_id:
        print('wrong user')
        return HttpResponseRedirect('/rsvp/confirm/{invite_id}/'.format(invite_id=request.user.username))



    return render(request, template_name='guests/rsvp_confirmation.html', context={
        'party': party,
    })




def _base64_encode(filepath):
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read())
