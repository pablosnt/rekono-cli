Thank you for making Rekono greater.

## Issues

You can create different kinds of [Issues](https://github.com/pablosnt/rekono-cli/issues/new/choose) to report bugs, request new features or ask for help.

Please, don't report security vulnerabilities in GitHub Issues. See our [Security Policy](https://github.com/pablosnt/rekono-cli/security/policy).


## Contributing to Rekono

You can create Pull Requests to the `develop` branch of this project. All the Pull Requests should be reviewed and approved before been merged. After that, your code will be included on the next Rekono release.

In this section you can see how to achieve that and the things that you should to take into account.

### Development environment

You can follow the [`From Source`](https://github.com/pablosnt/rekono-cli#from-source) installation guide to prepare your development environment.

### CI/CD

This project has the following checks in _Continuous Integration_:

1. `Code style`: check the source code style using the tools `mypy`, `flake8` and `eslint`.

2. `SCA`: check the project dependencies to find libraries with known vulnerabilities. Software Composition Analysis.

3. `Secrets scanning`: check the source code to find leaked passwords, tokens or other credentials that could be exposed in the GitHub repository.

**All CI/CD checks should be passed before merging any Pull Request**, so it's advised to install the pre-commit hooks in your local repositories using this commands:

```
# pwd: root directory
python3 -m pip install pre-commit
pre-commit install
```

### Way of Code

There are some guidelines to keep the code clean and ensure the correct working of the application:

- Comment your code, specially to document the classes and methods.
- Don't include code vulnerabilities or vulnerable libraries.
