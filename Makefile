.PHONY: build build-jupyter-lite clear-jupyter-outputs

build:
	rm -rf dist
	.venv/bin/python3 -m pip install --upgrade build
	.venv/bin/python3 -m build

# build-jupyter-lite:
# 	rm -rf dist/jupyterlite-site
# 	mkdir -p dist/jupyterlite-site
# 	.venv/bin/jupyter lite build \
# 		--contents jupyter \
# 		--output-dir dist/jupyterlite-site

build-jupyter-lite:
	rm -rf dist/jupyterlite-site
	mkdir -p dist/jupyterlite-site
	rm -rf dist/tmp-files
	mkdir -p dist/tmp-files
	cp -R mashcima2 dist/tmp-files/mashcima2/
	cp -R jupyter/. dist/tmp-files/
	.venv/bin/jupyter lite build \
		--contents dist/tmp-files \
		--output-dir dist/jupyterlite-site
	rm -rf dist/tmp-files

clear-jupyter-outputs:
	.venv/bin/jupyter nbconvert --clear-output --inplace jupyter/*.ipynb
