# Python API client for WikiPathways webservices.

## How to Use

Clone and `cd` into this repo:

```
git clone https://github.com/wikipathways/wikipathways-api-client-py.git
cd wikipathways-api-client-py
```

Install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html) and create a new virtualenv:

```bash
mkvirtualenv your_preferred_name
```

Install `wikipathways-api-client-py`:

```
pip install -e .
```

Try one of the examples:

```
python ./examples/example_get_pathway_as.py
```

Now that your virtualenv is created, you can leave it whenever you like with:

```bash
deactivate
```

And come back to it later with:

```bash
workon your_preferred_name
```

To list all your virtualenvs:

```bash
ls $WORKON_HOME
```

## Supported API calls

The following API calls are supported. Feel free to make a pull request if
you write code to support any of the other calls!

- [x] listOrganisms
- [x] listPathways
- [x] getPathwayInfo
- [ ] getPathwayHistory
- [ ] getRecentChanges
- [ ] login
- [x] getPathwayAs
- [ ] updatePathway
- [x] createPathway
- [x] findPathwaysByText
- [x] findPathwaysByXref
- [ ] findInteractions
- [ ] saveCurationTag
- [ ] removeCurationTag
- [ ] getCurationTags
- [ ] getCurationTagsByName
- [x] getColoredPathway
- [ ] getXrefList
- [ ] findPathwaysByLiterature
- [ ] getOntologyTermsByPathway
- [ ] getOntologyTermsByOntology
- [ ] getPathwaysByOntologyTerm
- [ ] getPathwaysByParentOntologyTerm

## Future Enhancements
- [ ] Add tests
- [ ] Add documentation and build docs with PyDoc
- [ ] Publish on PyPI so it can be installed with ```pip```

