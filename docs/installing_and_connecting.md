# Installing and connecting

`migra` is written in Python and thus requires a recent version of Python to be installed. Make sure you use at least Python 3.6: `migra` will very soon stop supporting earlier versions (Python 2 will soon reach end-of-life anyway).

## Installing migra

Install migra and necessary dependencies with the usual `pip install`:

    :::bash
    pip install migra

This doesn't include the PostgreSQL driver, but you can install that separately, or at the same with:

    :::bash
    pip install migra[pg]

If you're on `zsh`, you'll need quote marks, as in: `'migra[pg]'`.


## Connecting

`migra` uses database URLs to specify database connections. If you're unfamiliar with these, they work very much like a URL, incorporating all the details necessary for making a database connection into one concise string.

The general form is as follows:

    :::bash
    connectiontype://username:password@databasehostname/databasename?extraparam1=a&extraparam2=b

If you have a .pgpass file in your $HOME dir, you can make use of that as well
as you don't need to enter the password in the connection string:

    :::bash
    postgresql://username@hostname/databasename

These can be left out if not necessary. For instance, if connecting locally, using your default system username and passwordless "trust" login, only a connection type and database name is required:

    :::bash
    postgresql:///exampledatabase

Note that all the slashes are still required, so there are three slashes in a row.

Alternate drivers can be specified with a `+` modifier to the connection type:

    :::bash
    postgresql+pg9000:///example

For further details, consult the `sqlalchemy` docs: This is what migra uses under the hood to do connections (via a wrapper module called `sqlbag`).

## Background: Installing python and pip

### Python

Your operating system may include Python, but possibly not the latest version. `migra` will always work best with the latest stable version of Python, so ideally install the latest stable release (as specified on [python.org](https://python.org/)).

On Windows/MacOS, you can use the installer from [python.org](https://python.org/). On linux, as always, this situation is more complicated: Your default OS repos often have version 2 installed by default, and if they have a separate version of Python 3 it won't be the latest one. You can add various external repos or build your own version from source. I wrote a tool called [autovenv](/docs/autovenv) that manages multiple python versions (and virtual environments). Feel free to try it (I use it on both MacOS and linux), but it may be buggy (it isn't yet production software).

### pip

Once you have python installed you need to install `pip`. This too can complicated - recent python versions automatically install pip too, but often OS-managed versions do not. Check that when you run `pip -V` that it runs the desired Python version you have installed.

## Aside: Virtual environments

`python` has the notion of `virtual environments` (often called `virtualenv`s or `venv`s) which create an isolated place to install external python packages separate from what might have already be installed by the operating system. It's generally good practice to use these when working with Python - but if you're not otherwise using Python and just need `migra` from the command line, these may not be worth bothering with.

