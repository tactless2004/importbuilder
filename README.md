# ImportBuilder :construction_worker:

Have you ever built a python project and forgot to use some sort of virtual environment or depedency manager? You could `pip freeze` and add every python package you have ever installed on your OS. Or, you could make a fresh virtualenv and run the project, installing a new module into the env each time you get a `ModuleNotFoundError`.

**ImportBuilder** solves this problem. It searches through your project finding each dependency and determines the correct installed version by searching your site packages. Ultimately creating a pip compatible `requirements.txt` file.

## Install 
**ImportBuilder** uses Python3.12 or later.

## Usage
Run **importbuilder** on a python project in a folder `my_project`, then write the requirements file to `reqs.txt`

```sh
python -m importbuilder -f my_project -o reqs.txt
```

## Roadmap

- [ ] Add PyPi API support
- [ ] Add PIP install subprocess to run the generated requirements file