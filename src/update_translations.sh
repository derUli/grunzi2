pybabel extract . -o resources/locales/base.pot
pybabel update -i resources/locales/base.pot -d resources/locales
pybabel compile -d resources/locales --use-fuzzy