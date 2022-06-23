SHELL = /bin/bash -e
ROOTDIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python3 --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
python_version_patch := $(word 3,${python_version_full})

python_version_major_desired := 3
python_version_minor_desired := 7



setup: venv requirements
	echo done

# ignore this for now
python-version:
	@if [ $(python_version_major) -ne $(python_version_major_desired) ]; then\
		echo "python major version doesn't match: expected $(python_version_major_desired) found $(python_version_major) "; exit 1;\
	fi
	@if [ $(python_version_minor) -ne $(python_version_minor_desired) ]; then\
		echo "python minor version doesn't match: expected $(python_version_minor_desired) found $(python_version_minor) "; exit 1;\
	fi

.PHONY: venv
venv:
ifeq ($(wildcard $(ROOTDIR)/venv/.),)
	python3 -m venv venv
endif
	source $(ROOTDIR)/venv/bin/activate

requirements:
	# install pip dependencies
	pip3 install -r requirements.txt


clean:
	-rm -rf $(ROOTDIR)/__pycache__
	-deactivate
	-rm -rf $(ROOTDIR)/venv
	
dev:
	echo dev

run:
	python3 $(ROOTDIR)/app.py

connect:
	# chmod  400 ~/.ssh/id_rsa
	echo "Looking in " $(ROOTDIR)/aws_login.pem " for key..."
	ssh -i $(ROOTDIR)/aws_login.pem ec2-user@ec2-44-204-74-64.compute-1.amazonaws.com