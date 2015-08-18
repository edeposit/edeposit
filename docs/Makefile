# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

PNGS = uc01.png uc02.png uc03.png uc04.png uc04.svg uc05.png uc06.png uc07.png uc08.png uc15.png pm01.png pm02.png pm03.png pm04.png pm05.png pm06.png processmodels.png pm07.png pm08.png dm01.png dm02.png dm03.png architecture.png uc12.png uc13.png wf01.png wf02.png wf04.png dm04.png wf03.png wf03.svg middleware/dm01.png middleware/seq01.png middleware/dm00.png middleware/dm02.png middleware/component01.png uc14.png middleware/seq02.png middleware/dm03.png middleware/dm04.png plans/plan-nasazeni.html architecture.svg servers.png servers.svg

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  pickle     to make pickle files"
	@echo "  json       to make JSON files"
	@echo "  htmlhelp   to make HTML files and a HTML help project"
	@echo "  qthelp     to make HTML files and a qthelp project"
	@echo "  devhelp    to make HTML files and a Devhelp project"
	@echo "  epub       to make an epub"
	@echo "  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  latexpdf   to make LaTeX files and run them through pdflatex"
	@echo "  text       to make text files"
	@echo "  man        to make manual pages"
	@echo "  texinfo    to make Texinfo files"
	@echo "  info       to make Texinfo files and run them through makeinfo"
	@echo "  gettext    to make PO message catalogs"
	@echo "  changes    to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  doctest    to run all doctests embedded in the documentation (if enabled)"

clean:
	-rm -rf $(BUILDDIR)/*

html: $(PNGS)
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml: $(PNGS)
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

singlehtml: $(PNGS)
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

pickle: $(PNGS)
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json: $(PNGS)
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp: $(PNGS)
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

qthelp: $(PNGS)
	$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
	@echo
	@echo "Build finished; now you can run "qcollectiongenerator" with the" \
	      ".qhcp project file in $(BUILDDIR)/qthelp, like this:"
	@echo "# qcollectiongenerator $(BUILDDIR)/qthelp/E-Deposit.qhcp"
	@echo "To view the help file:"
	@echo "# assistant -collectionFile $(BUILDDIR)/qthelp/E-Deposit.qhc"

devhelp: $(PNGS)
	$(SPHINXBUILD) -b devhelp $(ALLSPHINXOPTS) $(BUILDDIR)/devhelp
	@echo
	@echo "Build finished."
	@echo "To view the help file:"
	@echo "# mkdir -p $$HOME/.local/share/devhelp/E-Deposit"
	@echo "# ln -s $(BUILDDIR)/devhelp $$HOME/.local/share/devhelp/E-Deposit"
	@echo "# devhelp"

epub: $(PNGS)
	$(SPHINXBUILD) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

pdf: $(PNGS)
	$(SPHINXBUILD) -bpdf $(ALLSPHINXOPTS) . $(BUILDDIR)/pdf
	@echo
	@echo "Build finished; the PDF files are in $(BUILDDIR)/pdf."

latex: $(PNGS)
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."

latexpdf: $(PNGS)
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

text:
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo
	@echo "Build finished. The text files are in $(BUILDDIR)/text."

man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	@echo
	@echo "Build finished. The manual pages are in $(BUILDDIR)/man."

texinfo:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo
	@echo "Build finished. The Texinfo files are in $(BUILDDIR)/texinfo."
	@echo "Run \`make' in that directory to run these through makeinfo" \
	      "(use \`make info' here to do that automatically)."

info:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo "Running Texinfo files through makeinfo..."
	make -C $(BUILDDIR)/texinfo info
	@echo "makeinfo finished; the Info files are in $(BUILDDIR)/texinfo."

gettext:
	$(SPHINXBUILD) -b gettext $(I18NSPHINXOPTS) $(BUILDDIR)/locale
	@echo
	@echo "Build finished. The message catalogs are in $(BUILDDIR)/locale."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."


uc01.png: uc01.plantuml
	java -jar ~/lib/plantuml.jar $?

uc02.png: uc02.plantuml
	java -jar ~/lib/plantuml.jar $?

uc03.png: uc03.plantuml
	java -jar ~/lib/plantuml.jar $?

uc04.png: uc04.plantuml
	java -jar ~/lib/plantuml.jar $?

uc04.svg: uc04.plantuml
	java -jar ~/lib/plantuml.jar -tsvg $?

uc05.png: uc05.plantuml
	java -jar ~/lib/plantuml.jar $?

uc06.png: uc06.plantuml
	java -jar ~/lib/plantuml.jar $?

uc07.png: uc07.plantuml
	java -jar ~/lib/plantuml.jar $?

uc08.png: uc08.plantuml
	java -jar ~/lib/plantuml.jar $?

uc15.png: uc15.plantuml
	java -jar ~/lib/plantuml.jar $?

processmodels.png: processmodels.plantuml
	java -jar ~/lib/plantuml.jar $?

pm01.png: pm01.plantuml
	java -jar ~/lib/plantuml.jar $?

pm02.png: pm02.plantuml
	java -jar ~/lib/plantuml.jar $?

pm03.png: pm03.plantuml
	java -jar ~/lib/plantuml.jar $?

pm04.png: pm04.plantuml
	java -jar ~/lib/plantuml.jar $?

pm05.png: pm05.plantuml
	java -jar ~/lib/plantuml.jar $?

pm06.png: pm06.plantuml
	java -jar ~/lib/plantuml.jar $?

pm07.png: pm07.plantuml
	java -jar ~/lib/plantuml.jar $?

pm08.png: pm08.plantuml
	java -jar ~/lib/plantuml.jar $?

dm01.png: dm01.plantuml
	java -jar ~/lib/plantuml.jar $?

dm02.png: dm02.plantuml
	java -jar ~/lib/plantuml.jar $?

dm03.png: dm03.plantuml
	java -jar ~/lib/plantuml.jar $?

architecture.png: architecture.plantuml
	java -jar ~/lib/plantuml.jar $?

architecture.svg: architecture.plantuml
	java -jar ~/lib/plantuml.jar -tsvg $?

servers.png: servers.plantuml
	java -jar ~/lib/plantuml.jar $?

servers.svg: servers.plantuml
	java -jar ~/lib/plantuml.jar -tsvg $?

uc12.png: uc12.plantuml
	java -jar ~/lib/plantuml.jar $?

uc13.png: uc13.plantuml
	java -jar ~/lib/plantuml.jar $?

uc14.png: uc14.plantuml
	java -jar ~/lib/plantuml.jar $?

wf01.png: wf01.plantuml
	java -jar ~/lib/plantuml.jar $?

wf02.png: wf02.plantuml
	java -jar ~/lib/plantuml.jar $?

wf03.png: wf03.plantuml
	java -jar ~/lib/plantuml.jar $?

wf03.svg: wf03.plantuml
	java -jar ~/lib/plantuml.jar -tsvg $?

wf04.png: wf04.plantuml
	java -jar ~/lib/plantuml.jar $?

dm04.png: dm04.plantuml
	java -jar ~/lib/plantuml.jar $?

middleware/dm00.png: middleware/dm00.plantuml
	java -jar ~/lib/plantuml.jar $?

middleware/dm01.png: middleware/dm01.plantuml
	java -jar ~/lib/plantuml.jar $?

middleware/dm02.png: middleware/dm02.plantuml
	java -jar ~/lib/plantuml.jar $?

middleware/dm03.png: middleware/dm03.plantuml
	java -jar ~/lib/plantuml.jar $?

middleware/dm04.png: middleware/dm04.plantuml
	java -jar ~/lib/plantuml.jar $?

middleware/seq01.png: middleware/seq01.plantuml
	java -jar ~/lib/plantuml.jar $?

middleware/seq02.png: middleware/seq02.plantuml
	java -jar ~/lib/plantuml.jar $?

middleware/component01.png: middleware/component01.plantuml
	java -jar ~/lib/plantuml.jar $?

plans/plan-nasazeni.html: plan-nasazeni.tjp
	rm -f _build/html/_static/plans/plan-nasazeni.html
	tj3 -o _static/plans $?
