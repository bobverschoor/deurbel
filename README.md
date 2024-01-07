# Deurbel

Deurbel is een applicatie met deurbel functionaliteit:

Een fysieke knop bij de deur wordt ingedrukt. 
Dit wordt gedetecteerd door de applicatie en een aantal acties worden uitgezet:
1. De gong wordt geluid
2. (optioneel) Een foto wordt genomen
3. (optioneel) Een bericht wordt gestuurd via Telegram, met daarin indien de foto.
4. (optioneel) Een trigger wordt gestuurd naar home assistant.

## Installatie
Dit is opgezet als een poetry project, dus poetry zal aanwezig moeten zijn, naast uiteraard een python executable (3.11).
Op de microcontroller (meestal de raspberry Pi) moet de package python3-RPi zijn geinstalleerd, 
maar deze is standaard onderdeel van raspbian dan wel micropython.

