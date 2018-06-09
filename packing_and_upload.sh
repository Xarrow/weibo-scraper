#!/usr/bin/env bash

echo ">>> running python setup.py sdist"
python setup.py sdist
echo ">>> running python setup.py bdist_wheel --universal"
python setup.py bdist_wheel --universal

echo ">>> running twine upload dist/* "
twine upload dist/*