STATIC_ANALYSER_IMAGE := "docker.onedata.org/python_static_analyser:v8"
GUI_FILES := gui/steps gui/meta_steps gui/utils gui/__init__.py
FILES_TO_FORMAT := gui/steps gui/meta_steps gui/utils gui/__init__.py gui/conftest.py

.PHONY: format

##
## Formatting
##

format:
	docker run --rm -i -v `pwd`:`pwd` -w `pwd`  $(STATIC_ANALYSER_IMAGE) isort $(FILES_TO_FORMAT) --settings-file configs/.pyproject.toml
	docker run --rm -i -v `pwd`:`pwd` -w `pwd`  $(STATIC_ANALYSER_IMAGE) black $(FILES_TO_FORMAT) --config configs/.pyproject.toml


black-check:
	docker run --rm -i -v `pwd`:`pwd` -w `pwd`  $(STATIC_ANALYSER_IMAGE) black $(FILES_TO_FORMAT) --check --config configs/.pyproject.toml || \
	 (echo "Code failed Black format checking. Please run 'make format' before commiting your changes. "; exit 1)

	
##
## Static analysis
##

static-analysis:	
	docker run --rm -i -v `pwd`:`pwd` -w `pwd`  $(STATIC_ANALYSER_IMAGE) pylint $(GUI_FILES) --recursive=y --rcfile=configs/.pylintrc
	docker run --rm -i -v `pwd`:`pwd` -w `pwd`  $(STATIC_ANALYSER_IMAGE) pylint gui/conftest.py --recursive=y \
	--disable=redefined-outer-name,import-outside-toplevel,protected-access,unused-argument --rcfile=configs/.pylintrc

