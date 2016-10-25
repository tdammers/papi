#!/bin/sh
(
    cat docs-src/header.html
    pandoc --toc -f rst -t html README.rst
    cat docs-src/footer.html
) > docs/index.html
cp docs-src/style.css docs/style.css
