.PHONY: deploy ls destroy synth

STACK = "Demo$$DEMO"

ls:
	cdk ls --profile cdh

deploy:
	cdk deploy $(STACK) --profile cdh

destroy:
	cdk destroy $(STACK) --profile cdh

synth:
	cdk synth $(STACK) --profile cdh