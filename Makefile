package_name = gumo-datastore

export PATH := venv/bin:$(shell echo ${PATH})

.PHONY: setup
setup:
	[ -d venv ] || python3 -m venv venv
	pip3 install --ignore-installed twine wheel pytest pip-tools
	pip3 install --ignore-installed -r requirements.txt

.PHONY: release
release: clean build
	python3 -m twine upload \
		--repository-url https://upload.pypi.org/legacy/ \
		dist/*

.PHONY: test-release
test-release: clean build
	python3 -m twine upload \
		--repository-url https://test.pypi.org/legacy/ \
		dist/*

.PHONY: test-install
test-install:
	pip3 --no-cache-dir install --upgrade \
		-i https://test.pypi.org/simple/ \
		${package_name}

.PHONY: build
build:
	python3 setup.py sdist bdist_wheel

.PHONY: clean
clean:
	rm -rf $(subst -,_,${package_name}).egg-info dist build

.PHONY: pip-compile
pip-compile:
	pip-compile --upgrade-package gumo-core --output-file requirements.txt requirements.in
	pip3 install --ignore-installed -r requirements.txt

.PHONY: test
test: build
	pip3 install dist/${package_name}*.tar.gz
	./tests/run.sh

.PHONY: emulator-start emulator-stop run-sample
emulator-start:
	docker-compose up --detach

emulator-stop:
	docker-compose stop

run-sample: emulator-start
	GOOGLE_CLOUD_PROJECT=gumo-datastore \
		DATASTORE_EMULATOR_HOST=127.0.0.1:8081 \
		python sample/main.py
