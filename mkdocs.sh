#!/bin/sh
PACKAGE_VERSION=$(python setup.py --version)
(
    cat docs-src/header.html
    pandoc --toc -f rst -t html README.rst
    cat docs-src/footer.html
) > docs/index.html
cp docs-src/style.css docs/style.css
cd docs
zip "../dist/papi-$PACKAGE_VERSION-docs.zip" *
cd ..
