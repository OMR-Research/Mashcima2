.PHONY: build demo-serve clear-jupyter-outputs

build:
	rm -rf dist
	.venv/bin/python3 -m pip install --upgrade build
	.venv/bin/python3 -m build

demo-serve:
	.venv/bin/voila --no-browser --port 8866 jupyter/

clear-jupyter-outputs:
	.venv/bin/jupyter nbconvert --clear-output --inplace jupyter/*.ipynb
