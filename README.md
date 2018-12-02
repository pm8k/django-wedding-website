# A Django Wedding Website and Invitation + Guest Management System


## A note from pm8k:

I used a fork of czue's repo as a base for what I accomplished. A lot of the ReadMe below is directly taken from his Readme, with alterations where I customized the website to my requirements. Please reference his as well if there is something unclear. I've removed bits of the readme that don't apply to my version, and will **bold** additional comments from me.

Live site examples:

- [Standard Wedding Website](http://marmerwedding.com/)
- **czue's implementation included supervisord deployment details. I however did not need these, as I leveraged pythonanywhere.com to host my site.**

## What's included?

This includes everything we did for our own wedding:

- A responsive, single-page traditional wedding website
- A complete guest management application
- Email framework for invitations and built in RSVP system
- Guest dashboard

More details on these below.

### The "Standard" Wedding Website

The standard wedding website is a responsive, single-page, twitter bootstrap-based site (using a modified version of
[this theme](https://blackrockdigital.github.io/startbootstrap-creative/)).

It is completely customizable to your needs and the content is laid out in standard django templates. By default it includes:

- A "hero" splash screen for a photo
- A mobile-friendly top nav with scrollspy
- A photo/hover navigation pane
- Configurable content sections for every aspect of your site that you want
- A set of different styles you can use for different sections

![Hero Section of Wedding Website](https://raw.githubusercontent.com/pm8k/django-wedding-website/master/screenshots/hero-page.png)

### Guest management

The guest management functionality acts as a central place for you to manage your entire guest list.
It includes two data models - the `Party` and the `Guest`.

#### Party model

The `Party` model allows you to group your guests together for things like sending a single invitation to a couple.
You can also add parties that you're not sure you're going to invite using the `is_invited` field, which works great for sending tiered invitations.
There's also a field to track whether the party is invited to the rehearsal dinner.
**I also added an additional field if they are bringing a plus one. Part of the party configuration contains a boolean flag if that party has a plus one invite available**

#### Guest model

The `Guest` model contains all of your individual guests.
In addition to standard name/email it has fields to represent whether the guest is a child (for kids meals/pricing differences),
and, after sending invitations, marking whether the guest is attending and what meal they are having.

#### Excel import/export

The guest list can be imported and exported via excel (csv).
This allows you to build your guest list in Excel and get it into the system in a single step.
It also lets you export the data to share with others or for whatever else you need.

See the `import_guests` management command for more details and `bigday/guests/tests/data` for sample file formats.

### Save the Dates

** I removed the save the date functionality from our site, as we wanted to send physical save the dates. **

### Invitations and RSVPs

The app also comes with a built-in invitation system.
The template is similar to the save-the-date template, however in addition to the standard invitation content it includes:


- Online RSVP system with meal selection and validation
- **Unique login for each party, with names prepopulated for all members of the party, and drop downs for each guest in the party**
- **The script guests/create_users.py is what loads in user login information. Test examples can also be found in bigday/tests/data**
### Guest dashboard

After your invitations go out you can use the guest dashboard to see how many people have RSVP'd, everyone who still
has to respond, people who haven't selected a meal, etc.
It's a great way of tracking your big picture numbers in terms of how many guests to expect.

Just access `/dashboard/` from an account with admin access. Your other guests won't be able to see it.

![Wedding Dashboard](https://raw.githubusercontent.com/pm8k/django-wedding-website/master/screenshots/wedding-dashboard.png)

### Other details

You can easily hook up Google analytics by editing the tracking ID in `google-analytics.html`.
**I haven't tested this piece**

## Installation

It's recommended that you setup a virtualenv before development.

Then just install requirements, migrate, and runserver to get started:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Customization

**As czue stated on his repo, all of this is customized for my needs, so feel free to customize it yourself. Feel free to raise issues or reach out to me if you have any questions/comments. Thanks!

-Matt**
