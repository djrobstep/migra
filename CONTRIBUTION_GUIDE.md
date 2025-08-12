# Contribution guide


## Quirks

All tests must be unsafe operations - i.e. must thave a `DROP` statement somewhere in the sql generated for the migration generated (i.e. setting a comment to `IS NULL`) does not count as a drop

## Installation

1. Clone the [schemainspect](https://github.com/PhilipWee/schemainspect) repository to the same directory as this one
2. Update the `pyproject.toml` to point to your current `schemainspect` installation (Instead of the published one)
3. Run `poetry update` to update your dependencies
4. Install either `postgres 16/17` on your computer, and make sure it is exposed on port `5432`
5. Create a super user in your postgres with a username matching your computer's username
6. Run `pytest` to make sure all test cases pass

## Contributing

1. Read the [Architecture](ARCHITECTURE.md) to get an idea of how everything links together
2. Make the changes you need to make in `schemainspect`
3. Create the test cases needed in `schemainspect` (The `schemainspect` test cases only pass on `pg<=15`, but for most intents and purposes, your specific test case should pass, you can let the CICD check whether it actually works on `pg<=15`)
4. Make the changes you need to make in `migra`
5. Under `tests/FIXTURES`, copy one of the existing test cases as a template. 
6. Add your fixture under `test_migra.py`
7. Run your test with `pytest -svv -k your-test-name-pattern`
8. If your test passes, run the remaining tests
9. Open a PR!!! Woohoo!

## Trust the process

Up until recently, `migra` had a very laissez-faire approach to contributions, but that created a few issues that made it harder for maintainers to review and left PRs languishing for too long.

This new contributions guidelines are aimed to fix that, while still making contributing easy and approachable.

Make sure your contribution follows these steps:

- Before getting into code, raise an issue - maintainers should have useful advice on how to approach the change. Build some basic consensus on the approach before coding.

- Break the fix/feature/change into several smaller changes. Most changes will also involve changing `schemainspect` at the same time, which does most of the gruntwork under the hood of migra.

- Keep the individual PRs extremely small. 100 lines or less ideally. This one is key for making them quick and easy to review.

## Meet the maintainers

Your humble team of maintainers currently consists of the following folks:

- @djrobstep (original author)
- @maximsmol, @kennyworkman, @aidanabd (new volunteers from latch.bio)
- @philipwee (current maintainer)

