# Requirements

You need to have an account in pingen and obtain oauth credentials for your desired grant type (usually client_credentials).

How to obtain these are described here: https://api.pingen.com/documentation#section/Authentication/How-to-obtain-a-Client-ID

Python 3.8+

# Installation

You don't need this source code unless you want to modify the package. If you just want to use the package, just run:

```sh
pip install --upgrade pingen2sdk
```

# Environments

We have two Environments available: Production and Staging (see https://api.pingen.com/documentation#section/Basics/Environments)

This SDK supports staging as well. **When initiating the resource** (see Usage), the optional 'staging' attribute should be set, **as well as when creating an endpoint object**.

# Usage

The simplest way to integrate is using the client credentials grant (see https://api.pingen.com/documentation#section/Authentication/Which-grant-type-should-i-use)

```python
import pingen2sdk

pingen2sdk.client_id = "YOUR_CLIENT_ID"
pingen2sdk.client_secret = "YOU_SECRET"

resp = pingen2sdk.OAuth.get_token(
    use_staging=True,
    grant_type="client_credentials",
    scope="letter batch webhook organisation_read",
)

access_token = resp["access_token"]

organisationList = pingen2sdk.Organisations(access_token, True).get_collection()

organisation_id = organisationList.data["data"][0]["id"]

LettersEndpoint = pingen2sdk.Letters(organisation_id, access_token, True)

response = LettersEndpoint.upload_and_create(
    "./letter.pdf",
    "sdk.pdf",
    "left",
    False,
    "fast",
    "simplex",
    "color",
)

letter_id = response.data["data"]["id"]
```

# Examples & Docs

Our API Docs are here: https://api.pingen.com/documentation

On the right-hand side of every endpoint you can see request samples for Python and other languages, which you can copy and paste into your application.

# Bugreport & Contribution

If you find a bug, please either create a ticket in github, or initiate a pull request.

# Versioning

We adhere to semantic (major.minor.patch) versioning (https://semver.org/). This means that:
* Patch (x.x.patch) versions fix bugs
* Minor (x.minor.x) versions introduce new, backwards compatible features or improve existing code.
* Major (major.x.x) versions introduce radical changes which are not backwards compatible.

In your automation or procedure you can always safely update patch & minor versions without the risk of your application failing.

# Testing

Run all tests for a specific Python version (modify `-e` according to your Python target):

```sh
tox -e py312
```

Run the linter with:

```sh
tox -e lint
```

The library uses Black for code formatting. Code must be formatted
with Black before PRs are submitted, otherwise CI will fail. Run the formatter
with:

```sh
tox -e fmt
```