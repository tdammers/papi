#!/bin/sh
(
    cat docs-src/header.html
    pandoc --toc -f markdown -t html README.markdown
    cat docs-src/footer.html
) > docs/index.html
cp docs-src/style.css docs/style.css
