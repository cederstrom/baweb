# -*- coding: utf-8 -*-
import os
from dateutil import parser


WTF_CSRF_ENABLED = True

# SQLAlchemy
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

FLUMRIDE = {
    'SUBMIT_OPEN': parser.parse("2022-04-09 12:00:00 +0100"),
    'SUBMIT_CLOSE': parser.parse("2022-04-29 20:00:00 +0100"),
    'YEAR': 'Tviitausen-tchjuh-tvauåh',
    'START_DATE': '6:e maj',
    'END_DATE': '8:e maj',
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
           '12:00 - 17:00: Incheckning sker utanför Multisalen i Karlskrona. Här delas flumpass, partykit™ och det finns även chans till att köpa capshandukar.',
           '16:00 - 17:30: Nu är det dags för en ny brutalspårrt? Slip`n`die vilket kommer äga rum precis utanför incheckningen, se till att ni har kompisar på röntgen.',
           '19:00 - 21:00 Sker den Olympiska Fyllan, direkt importerat från de gamla grekerna för att sedan avsluta kvällen på kårhuset Villan.']
        },
        {
            'day': 'Lördag',
            'data': ['12:00 - 15:00 Flumrundan, lunch serveras under tiden.',
             '18:00 - 20:00 Sittningen som ni kanske inte kommer ihåg i efterhand.',
             '20:00 - 21:00 ÖVERRASKNING',
             '21:00 - 02:00 Kårkväll på Villan.']
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
            'description': 'Sovsal (fredag och lördag) inkl. frukost, sittning, flumrunda med spårrter och "lagom" mycket dônk (är detta året vi faktiskt ska dricka upp allt?), lunch på lördag, ett fräckt märke, två kårkvällar',
            'max_nr': 60
        },
        {
            'name': 'Kundvagnspasset',
            'price': 299,
            'description': 'Allt i kånntainerpasset minus sovsal och frukost',
            'max_nr': 250
        }
    ],
    'payment': {
        'last_payment_date': '2022-04-30',
        'bank': 'Swedbank',
        'account_number': '8214,704 294 840'
    },
    'MAX_NR_OF_MEMBERS': 10,
    'MAX_NR_OF_NOT_SFS': 60,
    'FACEBOOK_EVENT_URL': 'https://www.facebook.com/events/842160829812821',
    'TRAILER_URL': 'https://www.youtube.com/embed/r9AT5BzPg0Y'
}

FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/'
