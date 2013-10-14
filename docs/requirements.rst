Požadavky na systém a jeho omezení
----------------------------------------------------------------------------------------------------

Požadavky na funkci systému
...................................................

Požadavky které jsou kladeny na funkci systému.

1. Z pohledu producenta
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. systém umožňuje ukládat elektronické předlohy tištěných publikací :ref:`uc02-03`
#. systém umožňuje vkládat e-publikace licencované i Open Access e-publikace
#. systém umožňuje ohlašovat i tištěné publikace :ref:`uc02-01`
#. systém umožňuje doplňovat základní metadata e-publikace producentem
#. systém umožňuje vyměnit soubor i po přijetí akvizicí :ref:`uc02-10`
#. producent má možnost opravit metadata i po přijetí akvizicí :ref:`uc02-15`
#. systém umožňuje producentovi přidávat další soubory i po přijetí e-publikace akvizicí  :ref:`uc02-10`
#. e-publikace může obsahovat více souborů v různých formátech
#. systém poskytuje registraci producenta :ref:`uc01-02`
#. systém poskytuje producentovi zjednodušenou registraci jen na základě web registrace
#. systém umožňuje producentovi definovat podmínky užití a řídí se jimi = komu a jakým způsobem mohou být e-publikace zpřístupněny
#. systém přijímá i e-publikace s binárními přílohami
#. systém zobrazuje historii všech zadaných **ISBN** i těch, co prošly jinou cestou, než pres e-deposit
#. systém zobrazuje přehled o tom, co se s e-publikací děje, tj. sleduje změny v Alephu, Krameriovi :ref:`uc12-01`
#. systém informuje, jestli u vloženého souboru garantuje dlouhodobou ochranu
   nebo jen ochranu na binární úrovni

2. Z pohledu akvizice
~~~~~~~~~~~~~~~~~~~~~~~~

#. uložené soubory v systému kontroluje pracovník akvizice  :ref:`pm03`
#. systém zobrazuje **PDF** náhled
#. systém umožňuje zadávat základní bibliografický popis ručně
#. systém nabízí bibliografický popis načtený ze systému **Aleph**

3. Z pohledu systému
~~~~~~~~~~~~~~~~~~~~~~

#. každý soubor jedné e-publikace má žádný, nebo jeden, nebo více **ISBN** a může mít i jeden **ISSN**
#. tisková předloha má stejné **ISBN** jako tištěná publikace
#. e-publikace mohou být zpřístupněny za pomoci standardních rozhraní
#. systém při vkládání souboru vytváří **PDF** náhled 
#. systém informuje **Aleph**, že jsou e-publikace připraveny na doplnění bibliografických dat
#. systém načítá bibliografická data ze systému **Aleph**
#. systém ukládá e-publikace do systému **LTP** k trvalé archivaci
#. systém před uložením e-publikace do **LTP** provádí validaci natolik důkladnou, aby předešla odmítnutí na vstupu do **LTP**
#. do **LTP** se odesilaji data po katalogizaci
#. systém zjišťuje přítomnost virů ve vložených souborech
#. systém umí načítat e-periodika přes vlastní **ftp** server :ref:`uc07-03`, nebo z emailové schránky :ref:`uc07-04`
#. systém automaticky načítá údaje o publikacích, které byly zaregistrovány **ISBN agenturou**
#. systém umožňuje povolit jen přihlášení za pomoci hesla, přihlašovacího jména
#. systém si pamatuje všechny verze vloženého souboru
#. systém umí omezit přístup producenta na readonly přístup (např. při porušení smlouvy)
#. systém umí zakázat producenta přístup k jednotlivým e-publikacím (např. při porušení autorských práv)
#. systém umožňuje pdf náhled na soubory aniž by kopie opustila systém
#. systém umožňuje označit e-publikaci jako zakázanou (např. při zjištění, že byla autorem okopírována)
#. systém odesílá do Alephu i jednoznačnou linku na náhled e-publikace
#. systém nabízí u každé ePublikace proklik do Alephu pro jednoduché spuštění Alephu s dotyčnou ePublikací
#. v systému Aleph vzniká proklik na náhled e-publikace v e-deposit :ref:`uc03-03`
#. systém nabízí základní informační servis (počty přírůstků, zpřístupnění, ...) podle původců a typů dokumentů, ... :ref:`uc12`
#. systém provádí průběžnou zálohu vstupujících dokumentů
#. systém generuje různé náhledy, pro různé druhy zobrazení

Omezení systému
............................

#. systém zpřístupňuje pouze kopie
#. pokud e-publikace prošla akvizicí, producent má možnost jen přidávat opravy - jako další soubory. 
   Už nemůže editovat záznamy, soubory.
#. systém autorizuje uživatele vůči firemní **ActiveDirectory**, nebo vůčí **LDAP**
#. systém vytváří náhled v **PDF** ze všech formátů, kvuli akvizici a katalogizaci
#. systém poskytuje snadný způsob listování e-publikací, tj. náhledy po jednotlivých stránkách (hlavně pro katalogizaci, která musí celou e-publikaci prolistovat)
#. systém přijímá e-publikace v libovolném (binárním) formátu, dlouhodobou ochranu zaručuje pouze u formátů **ePub2** a **PDF/A**
#. systém nepřijímá publikace s ochranou proti kopírování, např **DRM**. 
   Publikaci přijme i s **DRM** pokud je v něm označení "Národní knihovna"
#. web rozhraní systému je poskytnuto za pomoci **Plone**
#. middleware k implementaci využívá **RabbitMQ**, tj. je implementován odděleně od web rozhraní
#. middleware je napsaný v jazyce **Python**

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
    
