.PHONY: build push-prod push-test demo-serve clear-jupyter-outputs

build:
	rm -rf dist
	.venv/bin/python3 -m pip install --upgrade build
	.venv/bin/python3 -m build

push-prod:
	.venv/bin/python3 -m pip install --upgrade twine
	.venv/bin/python3 -m twine upload dist/*

push-test:
	.venv/bin/python3 -m pip install --upgrade twine
	.venv/bin/python3 -m twine upload --repository testpypi dist/*

demo-serve:
	.venv/bin/voila --no-browser --port 8866 jupyter/

clear-jupyter-outputs:
	.venv/bin/jupyter nbconvert --clear-output --inplace jupyter/*.ipynb jupyter/*/*.ipynb jupyter/*/*/*.ipynb jupyter/*/*/*/*.ipynb
