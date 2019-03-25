coveragereport:
	coverage run nose_starter.py
	coverage html
	chromium-browser htmlcov/exerciseconverter_py.html

tests:
	clear
	py.test --cov-report html:cov_html --cov=src test/*.py

run_server:
	export FLASK_APP=web_converter.py && flask run

