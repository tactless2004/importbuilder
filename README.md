# ImportBuilder

Have you ever built a python project and forgot to use some sort of virtual environment or depedency manager? You could `pip freeze` and add every python package you have ever installed on your OS. Or, you could make a fresh virtualenv and run the project, installing a new module into the env each time you get a `ModuleNotFoundError`.

**ImportBuilder** solves this problem. It searches through your project finding each dependency and determines the correct installed version by searching your site packages. Ultimately creating a pip compatible `requirements.txt` file.