.. _acceptancetests:

Akceptační testy
................................


Hlavní scénáře k testování
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

- AT01 - Registrace producenta

  - `AT01-01 Registrace producenta bez editora <tests/at01.html#at01-01-registrace-producenta-bez-editora>`_
  - `AT01-03 Registrace producenta s editorem <tests/at01.html#at01-03-registrace-producenta-s-editorem>`_
  - `AT01-05 Registrace producenta s editorem - kontrola povinnych policek, shodnosti hesel <tests/at01.html#at01-05-registrace-producenta-s-editorem-kontrola-povinnych-policek-shodnosti-hesel>`_
  - `AT01-06 Kontrola zadaných hesel <tests/at01.html#at01-06-kontrola-zadanych-hesel>`_
  - `AT01-07 Kontrola dostupnosti uzivatelskeho jmena pri jedne registraci <tests/at01.html#at01-07-kontrola-dostupnosti-uzivatelskeho-jmena-pri-jedne-registraci>`_
  - `AT01-08 Kontrola dostupnosti uzivatelskeho jmena u editoru <tests/at01.html#at01-08-kontrola-dostupnosti-uzivatelskeho-jmena-u-editoru>`_
  - `AT01-12 Přidání nového editora k existujícímu producentovi a kontrola dostupnosti uzivatelskeho jmena <tests/at01.html#at01-12-pridani-noveho-editora-k-existujicimu-producentovi-a-kontrola-dostupnosti-uzivatelskeho-jmena>`_

- AT02 - Ohlášení ePublikace

  - `AT02-03 Ohlášení se soubory <tests/at02.html#at02-03-ohlaseni-se-soubory>`_
  - `AT02-05 Ohlášení se soubory co potrebuji generovani nahledu <tests/at02.html#at02-05-ohlaseni-se-soubory-co-potrebuji-generovani-nahledu>`_
  - `AT02-06 Ohlášení se soubory a pridelenim ISBN <tests/at02.html#at02-06-ohlaseni-se-soubory-a-pridelenim-isbn>`_

- AT03 - Akvizice

  - `AT03-07 Pracovní prostředí pracovníka ISBN agentury <tests/at03.html#at03-07-pracovni-prostredi-pracovnika-isbn-agentury>`_
  - `AT03-08 Pracovní prostředí administratora akvizice <tests/at03.html#at03-08-pracovni-prostredi-administratora-akvizice>`_

  

Všechny scénáře
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
.. toctree::
   :maxdepth: 2
   
   tests/at01
   tests/at02
   tests/at03
   tests/at04
   tests/at15

:download:`test report <tests/report.html>`

:download:`test log <tests/log.html>`

:download:`screenshot 1 <tests/selenium-screenshot-1.png>`
:download:`screenshot 2 <tests/selenium-screenshot-2.png>`

.. raw:: html

	<div id="disqus_thread"></div>
	<script type="text/javascript">
        /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
        var disqus_shortname = 'edeposit'; // required: replace example with your forum shortname

        /* * * DON'T EDIT BELOW THIS LINE * * */
        (function() {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        })();
	</script>
	<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
	<a href="http://disqus.com" class="dsq-brlink">comments powered by <span class="logo-disqus">Disqus</span></a>
    

