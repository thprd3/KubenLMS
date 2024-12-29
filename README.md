# KubenLMS

Dette er et modul-basert læringssystem for IM-elever skrevet i HTML/CSS og Python (Flask) med en Sqlite-database. 

## Funksjonalitet

Elever har tilgang til en oversikt over alle moduler, og en side for hver modul. Når en elev mener de har fulltført en modul, blir dette registrert i en kø som lærerne kan se. Lærere kan godkjenne eller underkjenne gjennomføringen. 

Moduler kan være låst bak andre moduler ("dependencies"). 

## To-Do:
* implementere autentisering og tilgangsstyring (elev og lærer)
* kunnskapsbase - wiki?

## Opprinnelige notater:

Brukersti:
* Elev velger og gjennomfører en modul. Melder selv til godkjenning når h*n er ferdig i systemet. Meldingen går til en "vurderingskø" som lærerne kan se.
* Lærer godkjenner (eller avviser? kanskje ikke nødvendig) etter praktisk vurdering og registrerer dommen i systemet.

Struktur:
* Moduler kan være låst inntil andre moduler er gjennomført.
* Moduler består av informasjon og oppgaver.

Kontekst:
* Etter x antall moduler gjør eleven et "prosjekt". Disse kan gjerne eksistere utenom systemet. 
* Målet med modulene er innlæring. Målet med prosjektene er utprøving, konsolidering, og vurdering.
