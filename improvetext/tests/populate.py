
from improvetext.models import Text
from improvetext.models import Type
from improvetext.models import Question

brief = Type()
brief.name = "Brief (standaard)"
brief.header = "Te beoordelen tekst"
brief.rating_header = "Geef uw waardering"
brief.comment_header = "Geef een reactie"
brief.save()


q1 = Question()
q1.position = 0
q1.question = "Is de brief duidelijk?"
q1.type = brief
q1.save()

q2 = Question()
q2.position = 1
q2.question = "Is de brief leesbaar?"
q2.type = brief
q2.save()

text = Text()
text.type = brief
text.title = "Brief 1: Koolmonoxidevergiftiging"
text.body = """<p><strong>Beste &lt;naam&gt;,</strong></p>

<p>De brandweer heeft uw adres aan ons doorgegeven omdat er bij u thuis een zeer ernstige situatie was geweest met koolmonoxide uit uw geiser/kachel/cv. U bent vast erg geschrokken. Koolmonoxide is gevaarlijk voor de gezondheid. GGD Haaglanden bewaakt en beschermt de gezondheid, daarom nemen wij contact met u op.
</p>
<p><strong>Belangrijk:</strong>
</p>
<p>• Schakel de geiser niet meer in totdat hij gerepareerd is.<br />
• Maak een afspraak met een erkend bedrijf om de geiser te repareren of te vervangen.<br />
• Bel daarna de Haagse Pandenbrigade (14070).<br />
</p>
<p>Zij controleren of er geen koolmonoxide meer vrij komt.
</p>
<p><strong>Het gevaar van koolmonoxide</strong>
</p>
<p>De GGD geeft informatie over het gevaar van koolmonoxide. Wij kunnen uw vragen beantwoorden, uitleggen hoe koolmonoxide ontstaat en wanneer het tot klachten kan leiden. Daarnaast geven wij u tips om de kans op koolmonoxide(ongelukken) in de toekomst te verkleinen. Leest u daarom ook de folder die bij deze brief zit. Heeft u na het lezen van de folder nog vragen, dan kunt u mij bereiken op het telefoonnummer (070) 353 71 82 of e-mailen naar gezondheidenmilieu@ggdhaaglanden.nl.
</p>
<p>Koolmonoxide is een dodelijk gas. Als u nu nog gezondheidsklachten heeft neemt u dan contact op met uw huisarts. Vertel hem dat u koolmonoxide heeft ingeademd.
</p>
<p><strong>Enquêteformulier</strong>
</p>
<p>Bij deze brief zit ook een enquêteformulier. De GGD Haaglanden wil graag weten hoeveel mensen gezondheids- klachten hebben door koolmonoxide(ongelukken). Daar is nog geen goed beeld van. Zou u de enquête willen invullen en terugsturen?
</p>
<p>Heeft u liever persoonlijk of telefonisch contact om de enquête in te vullen bel dan met (070) 353 71 82.
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