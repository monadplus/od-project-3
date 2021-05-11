(TeX-add-style-hook
 "preamble"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("babel" "english") ("algorithm2e" "vlined" "ruled") ("glossaries" "acronym")))
   (add-to-list 'LaTeX-verbatim-environments-local "minted")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "inputenc"
    "babel"
    "hyperref"
    "parskip"
    "tocbibind"
    "abstract"
    "graphicx"
    "amsmath"
    "amssymb"
    "bm"
    "amsthm"
    "minted"
    "algorithm2e"
    "xcolor"
    "glossaries"
    "enumitem")
   (TeX-add-symbols
    '("code" 1))
   (LaTeX-add-environments
    '("claimproof" 1)
    '("claim" 1))
   (LaTeX-add-amsthm-newtheorems
    "theorem"
    "corollary"
    "lemma"
    "definition"
    "remark")
   (LaTeX-add-xcolor-definecolors
    "codegray"))
 :latex)

