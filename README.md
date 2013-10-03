Name, States served, Internet address, Postal Address and Email Address of
public health insurances in Germany. To understand how the health system
in Germany works, please see [this Wikipedia article][wikipedia].

## Source

The data is sourced from a PDF made available by the [GKV-Spitzenverband][GKV]
from their [online database of health insurances][db]. The dataset is based on 
a version from 06.12.12, and already needs updating.

We started by doing everything manually, but then moved to extracting the data 
from the PDF using code from [this Gist][gist] which was then extended
to also find and parse the "Impressum" (Imprint/Legal contact information) of each site
and attempt to grab an email address, running on [ScraperWiki][swiki]. The extended script
is in the scripts folder. Missing emails, phone numbers and street addresses 
were taken manually. The working data set is on [Google Spreadsheets][gss].

[wikipedia]: http://en.wikipedia.org/wiki/Healthcare_in_Germany
[GKV]: http://www.gkv-spitzenverband.de/
[db]: http://www.gkv-spitzenverband.de/krankenversicherung/krankenversicherung_grundprinzipien/alle_gesetzlichen_krankenkassen/alle_gesetzlichen_krankenkassen.jsp
[gist]: https://gist.github.com/psychemedia/5800840
[gss]: https://docs.google.com/spreadsheet/ccc?key=0Ak6K0pSAyW1gdE0tWGtFam9FdXB1TFUyM2I3bzVZSXc
[swiki]: https://scraperwiki.com/‎


