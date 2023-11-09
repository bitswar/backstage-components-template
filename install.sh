#! /bin/bash
git clone https://github.com/bitswar/backstage-components-template bst-temp
mv bst-temp/catalog catalog
rm -rf bst-temp
rm $0