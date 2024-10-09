STATIC_ANALYSER_IMAGE := "docker.onedata.org/python_static_analyser:v8"

.PHONY: format

##
## Formatting
##

format:
	docker run --rm -i -v `pwd`:`pwd` -w `pwd`  $(STATIC_ANALYSER_IMAGE) isort gui/steps gui/meta_steps gui/scenarios gui/utils --settings-file configs/.pyproject.toml
	docker run --rm -i -v `pwd`:`pwd` -w `pwd`  $(STATIC_ANALYSER_IMAGE) black gui/steps gui/meta_steps gui/scenarios gui/utils --config configs/.pyproject.toml


black-check:
	docker run --rm -i -v `pwd`:`pwd` -w `pwd`  $(STATIC_ANALYSER_IMAGE) black gui/steps gui/meta_steps gui/scenarios gui/utils --check --config configs/.pyproject.toml || \
	 (echo "Code failed Black format checking. Please run 'make format' before commiting your changes. "; exit 1)

	
##
## Static analysis
##

static-analysis:	
	docker run --rm -i -v `pwd`:`pwd` -w `pwd`  $(STATIC_ANALYSER_IMAGE) pylint gui/steps gui/meta_steps gui/utils --recursive=y --rcfile=configs/.pylintrc

