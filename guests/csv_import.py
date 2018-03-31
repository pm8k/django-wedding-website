import csv
import StringIO
import uuid
from guests.models import Party, Guest


def import_guests(path):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            #party_name, first_name, last_name, party_type, is_child, category, is_invited, email = row[:8]
            party,first_name,last_name,plus_one,is_child,category,rehearsal_dinner = row[:7]

            if not party_name:
                print 'skipping row {}'.format(row)
                continue
            party = Party.objects.get_or_create(name=party_name)[0]
            party.category = category
            party.invitation_id = party
            party.save()

            guest = Guest.objects.get_or_create(party=party, first_name=first_name, last_name=last_name)[0]
            guest.is_child = is_child
            guest.save()


def export_guests():
    headers = [
        'party','first_name','last_name','plus_one','is_child',
        'category','is_attending','rehearsal_dinner','comments'
    ]
    file = StringIO.StringIO()
    writer = csv.writer(file)
    writer.writerow(headers)
    for party in Party.in_default_order():
        for guest in party.guest_set.all():
            if guest.is_attending:
                writer.writerow([
                    party.name,
                    guest.first_name,
                    guest.last_name,
                    party.plus_one,
                    guest.is_child,
                    party.category,
                    party.rehearsal_dinner,
                    guest.is_attending,
                    party.rehearsal_dinner,
                    party.comments,
                ])
    return file


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes')
