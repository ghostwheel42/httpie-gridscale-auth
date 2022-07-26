# httpie-gridscale-auth

gridscale authentication plugin for [HTTPie](https://httpie.org/).

## Installation

```bash
httpie plugins install httpie-gridscale-auth
```

or

```bash
pip install --upgrade httpie-gridscale-auth
```

You should now see `httpie-gridscale-auth` when running `httpie plugins list`.

## Usage

### Credentials on the CLI

The syntax and behavior is the same as with the basic auth.

```bash
http --auth-type gs --auth USERID:TOKEN https://api.gridscale.io/objects/locations
```

### Credentials via ``GRIDSCALE_*`` environment variables

The names are identical to what `gscloud` and other gridscale tools use, so you
might be already good to go.

```bash
export GRIDSCALE_UUID="<USERID>"
export GRIDSCALE_TOKEN="<TOKEN>"

http -A gs https://api.gridscale.io/objects/locations
```

### Credentials via local gridscale config

The plugin uses the configuration that `gscloud` and other gridscale tools use,
so you might be already good to go.

```bash
http --auth-type gs https://api.gridscale.io/objects/locations
```

It will use the project named "default" until you specify a project name or
gridscale userId like this:

```bash
http --auth-type gs --auth <NAME|USERID> https://api.gridscale.io/objects/locations
```
