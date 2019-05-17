# Run, Runner and Wheel

<img height="300" src="../../images/settings.png">

You can run job using either the formatted form or a pseudo cli.

## Formatted

For function completion and documentation, use the [parse module](settings.md#parse-modules) setting. Custom modules should also be present.

#### Target type


#### Target

This depends on the selected [Target type](#target-type).

#### Function

Function completion and documentation are taken from the [parse module](settings.md#parse-modules) setting.

#### Args and Keyword Arguments

Use these fields for functions. If functions use **named** args or kwargs, they should be suggested.

#### Schedule

Schedule a recurring job, or postpone it.

### Test button

The **test** button will run the selected function with `#!python test=True` kwarg set.

## CLI

This pseudo CLI should work like the salt command. Please refer to [Pepper](https://github.com/saltstack/pepper) documentation.