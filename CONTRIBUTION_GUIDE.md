# Contribution guide


## Installation

To make sure tests run on your system, you will need to have a local postgres db running with and provide the connection credentials to the test files so that the tests can be run

To do this:
1. Copy `.env.template` to `.env`
2. Fill in the relevant connection details. Leave `DB_PASSWORD` empty if no password is required
3. Run `pytest` to make sure that all test cases are able to pass

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

