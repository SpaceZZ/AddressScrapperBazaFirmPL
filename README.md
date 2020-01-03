# AddressScrapperBazaFirmPL

Web scrapping for the companies addresses database at www.baza-firm.com.pl

Uses Tesseract to OCR the images of the e-mails addresseses.

Tesseract needs to be downloaded to your machine.

1. Change the domain to the correct link, as per desired voivodeship. Currently it is https://www.baza-firm.com.pl/wojewodztwo/mazowieckie/strona-

2. Change the range of pages (just check last page and put the number in the for iterator for i in range(1, last page)
