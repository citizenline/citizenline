# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

from bettertexts.models import Question
from bettertexts.models import Text
from bettertexts.models import Type


class Command(BaseCommand):
    help = 'Populates with test data'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # base_domain = "citizenline.local:8000"
        base_domain = "citizenline.nl"

        s0 = Site.objects.get_or_create(pk=1, defaults={"domain": "example.com"})[0]
        s0.domain = "www-test." + base_domain
        s0.save()

        s1 = Site.objects.get_or_create(pk=2, defaults={"domain": "denhaag-test." + base_domain})[0]
        s1.save()

        brief = Type.objects.get_or_create(site=s1, name="Brief", defaults={
            "header": "Te beoordelen tekst",
            "rating_header": "Geef uw waardering",
            "comment_header": "Geef een reactie",
        })[0]
        brief.save()

        q1 = Question.objects.get_or_create(type=brief, position=0,defaults={
            "question": "Is de brief duidelijk?",
        })[0]
        q1.save()

        q2 = Question.objects.get_or_create(type=brief, position=1,defaults={
            "question": "Is de brief leesbaar?",
        })[0]
        q2.save()

        text = Text()
        text.site = s1
        text.type = brief
        text.title = "Brief 1: Koolmonoxidevergiftiging"
        text.body = """<p><strong>Beste &lt;naam&gt;,</strong></p>

        <p>De brandweer heeft uw adres aan ons doorgegeven omdat er bij u thuis een zeer ernstige situatie was geweest met koolmonoxide uit uw geiser/kachel/cv. U bent vast erg geschrokken. Koolmonoxide is gevaarlijk voor de gezondheid. GGD Haaglanden bewaakt en beschermt de gezondheid, daarom nemen wij contact met u op.
        </p>
        <p><strong>Belangrijk:</strong>
        </p>
        <p>• Schakel de geiser niet meer in totdat hij gerepareerd is.<br />
        • Maak een afspraak met een erkend bedrijf om de geiser te repareren of te vervangen.<br />
        • Bel daarna de lokale Pandenbrigade (1234567).<br />
        </p>
        <p>Zij controleren of er geen koolmonoxide meer vrij komt.
        </p>
        <p><strong>Het gevaar van koolmonoxide</strong>
        </p>
        <p>De GGD geeft informatie over het gevaar van koolmonoxide. Wij kunnen uw vragen beantwoorden, uitleggen hoe koolmonoxide ontstaat en wanneer het tot klachten kan leiden. Daarnaast geven wij u tips om de kans op koolmonoxide(ongelukken) in de toekomst te verkleinen. Leest u daarom ook de folder die bij deze brief zit. Heeft u na het lezen van de folder nog vragen, dan kunt u mij bereiken op het telefoonnummer (012) 345 67 89 of e-mailen naar gezondheidenmilieu@example.nl.
        </p>
        <p>Koolmonoxide is een dodelijk gas. Als u nu nog gezondheidsklachten heeft neemt u dan contact op met uw huisarts. Vertel hem dat u koolmonoxide heeft ingeademd.
        </p>
        <p><strong>Enquêteformulier</strong>
        </p>
        <p>Bij deze brief zit ook een enquêteformulier. De GGD in uw regio wil graag weten hoeveel mensen gezondheids- klachten hebben door koolmonoxide(ongelukken). Daar is nog geen goed beeld van. Zou u de enquête willen invullen en terugsturen?
        </p>
        <p>Heeft u liever persoonlijk of telefonisch contact om de enquête in te vullen bel dan met (012) 345 67 89.
        </p>
        <p>
        </p>
        <p>Met vriendelijke groet,
        </p>
        <p>Naam medewerker
        </p>
        """
        text.version = 0
        text.pub_date = "2016-02-01"
        text.save()
