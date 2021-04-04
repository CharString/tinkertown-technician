# Tinkertown Technician

## Developing
```sh
# Install dependencies
pip install --user pipx
pipx install pdm
pdm install --dev

# Setup pre-commit and pre-push hooks
pdm run pre-commit install -t pre-commit
pdm run pre-commit install -t pre-push
```
