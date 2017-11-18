### FORMATTING

```
autopep8 --in-place --aggressive --aggressive
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
