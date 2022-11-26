#!/usr/bin/env bash
echo ">>> delete exist packing "
rm -rf build
rm -rf dist
rm -rf weibo_scraper.egg-info
echo ">>> running python setup.py sdist"
python setup.py sdist
echo ">>> running python setup.py bdist_wheel --universal"
python setup.py bdist_wheel --universal

echo ">>> running twine check"
twine check sdist/*
echo ">>> running twine upload dist/* "
twine upload dist/* --skip-existing