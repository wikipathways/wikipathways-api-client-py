# Python API client for WikiPathways webservices.

## How to Use

Install virtualenvwrapper. Then:

```bash
mkvirtualenv your_preferred_name
pip install -e .
```

Once your virtualenv is created, you can come back to it with:

```bash
workon your_preferred_name
```

And leave it with:

```bash
deactivate
```

To list your virtualenvs:

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

