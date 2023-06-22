synth:
	cdk synth
deploy:
	cd src/msg-processor; pip install -r requirements.txt -t .
	cdk deploy --profile personal