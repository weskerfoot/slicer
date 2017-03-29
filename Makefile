default:
	virtualenv venv && source venv/bin/activate && pip install -r requirements.txt

run:
	source venv/bin/activate && ./slice.py ${DIR}
