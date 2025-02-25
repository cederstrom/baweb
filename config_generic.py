# -*- coding: utf-8 -*-
import os
from dateutil import parser

# SQLAlchemy
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

FLUMRIDE = {
    'SUBMIT_OPEN': parser.parse("2025-03-21 12:00:00 +0100"),
    'SUBMIT_CLOSE': parser.parse("2025-04-27 23:59:59 +0100"),
    'YEAR': 'Tjauge-che-fjem',
    'START_DATE': '2:e maj',
    'END_DATE': '4:e maj',
# EXAMPLE ON HOW TO FILL SCHEDULE DATA
#    [
#       {
#           'day': 'Fredag',
#           'data': [
#           'Brutalare från alla världens hörn anländer till Karlskrona ungefär samtidigt som alla tävlande.',
#           '12:00 - 18:00: Incheckning sker på kåren i Karlskrona. Här delas flumpass, partykit™ och lösa faddrar ut till alla anmälda.',
#           '18:00 - 20:00: VM i caps på kåren som efterföljs av tokröj tills samtliga personer har stupat (d.v.s. spik kl 21:00).'
#           ]
#       },
#       {
#           'day': 'Lördag',
#           'data': ['stuff', 'stuff2']
#       }
     'schedule': [
         {
             'day': 'Fredag',
             'data': ['Brutalare från alla världens hörn anländer till Karlskrona ungefär samtidigt som alla tävlande.',
             '16:00 - 18:00: Incheckning',
             '16:00 - 18:00: Slip n\' Die',
             '18:00 - 20:00: Vem vet vad som händer här?',
             '21:00 - 02:00: Kårkväll på Villan',
             '02:00 - gryningen: Efterphest (leta upp efterphestansvarig)']
         },
         {
             'day': 'Lördag',
             'data': ['13:00: - 16:00 Flumrundan, här kommer det att finnas korv till försäljning under tiden.',
             '16:15 - 16:30: Egghnikkning',
             '19:00 - 21:00: Sittningen som ni kanske inte kommer ihåg i efterhand',
             '21:00 - 02:00: Kårkväll på Villan',
             '02:00 - gryningen: Efterphest (leta upp efterphestansvarig)']
         },
         {
             'day': 'Söndag',
             'data': ["Nu är det dags att åka hem och börja återhämtningen till nästa år. Utcheckning sker senast 12:00."]
         }
     ],
    'ticket_types': [
        {
            'name': 'Kånntainerpasset',
            'price': 399,
            'description': 'Sovsal (fredag och lördag) inkl. frukost, sittning, flumrunda med spårrter och "lagom" mycket dônk (är detta året vi faktiskt ska dricka upp allt?), ett fräckt märke, två kårkvällar',
            'max_nr': 43
        },
        {
            'name': 'Kundvagnspasset',
            'price': 299,
            'description': 'Allt i kånntainerpasset minus sovsal och frukost',
            'max_nr': 190
        }
    ],
    'drink_options': [
        {
            'name': 'Två öl'
        },
        {
            'name': 'Två cider'
        },
        {
            'name': 'En öl och en cider'
        },
        {
            'name': 'Alkoholfritt'
        }
    ],
    'payment': {
        'last_payment_date': '2025-04-28',
        'bank': 'Theodor Qvarlander',
        'account_number': '0733241914'
    },
    'MAX_NR_OF_MEMBERS': 10,
    'MAX_NR_OF_NOT_SFS': 0,
    'FACEBOOK_EVENT_URL': 'https://www.facebook.com/events/585121854233476',
    'TRAILER_URL': 'https://www.youtube.com/embed/Iy7I1yaP4C8'
}

ÖHLREISE = {
    'SUBMIT_OPEN': parser.parse("2025-09-06 11:00:00 +0100"),
    'SUBMIT_CLOSE': parser.parse("2025-09-24 20:00:00 +0100"),
    'YEAR': 'Tjauge-che-fjem',
    'START_DATE': '27:e september',
    'END_DATE': '28:e september',
    'schedule': [
        {
            'day': 'Lördag',
            'data': ['07:00: Bussen lämnar campus, kom i god tid innan.',
            '08:45-09:15: Pit stop på Ekerödsrasten, kanske får du klappa en get?',
            '11:00-12:30: Bottleshop',
            '12:50-17:00: Fri lek i Köpendanmark',
            '17:00: Hemfärd, hemma någon gång mellan 21:00-22:45']
        }
    ],
    'ticket_types': [
        {
            'name': 'Åkpasset',
            'price': 399,
            'description': 'Vi ska åka fram och tillbaka till Köpendanmark, köpa en väldans massa öhl, och öhl kommer inmundigas. Du måste vara minst tjugo år för att få följa med på resan',
            'max_nr': 49
        }
    ],
    'payment': {
        'last_payment_date': '2025-09-26',
        'bank': 'Theodor Qvarlander',
        'account_number': '0733241914'
    },
    'FACEBOOK_EVENT_URL': 'https://www.facebook.com/events/473214195630248'
}

FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/'
