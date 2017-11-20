### COVERAGE

Aim for 100% coverage to ensure library will work with all specified python versions.

### FORMATTING

```
autopep8 --in-place --aggressive --aggressive
```

#### BUILDING DOCS

```
cd docs/
make clean html
open _build/html/index.html
```

### RELEASING

```
vi setup.py # increment version
git add ...
git commit -m '...'
git tag 0.0.9  -m "Add pypi python versions"
git push origin 0.0.9 
python setup.py sdist upload -r pypi
```
### Testing

Run all tests.

```
tox -e py27
```

Run single test.

```
pytest tests/doc/test_create_cluster.py
```
