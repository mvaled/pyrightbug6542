Showcase of bug [6542](https://github.com/microsoft/pyright/issues/6542)

Run like:

```
poetry install --sync
poetry run pyright
```

You'll get the output:

```
pyrightbug6542/demo/models.py
  pyrightbug6542/demo/models.py:20:16 - error: Cannot access member "dispose" for type "BaseManager[Tombstone]"
    Member "dispose" is unknown (reportGeneralTypeIssues)
1 error, 0 warnings, 0 informations 
```
