# Overview

This interface is for use with OpenStack Dashboard plugin subordinate charms.

# Usage

No explicit handler is required to consume this interface in charms
that consume this interface.

In addittion to the states automatically set based on relation data by
``charms.reactive.Endpoint``, the interface provides the
``{endpoint_name}.available`` state.

Properties for ``release``, ``bin_path``, and ``openstack_dir`` are also
provided.

# metadata

To consume this interface in your charm or layer, add the following to `layer.yaml`:

```yaml
includes: ['interface:dashboard-plugin']
```

and add a requires interface of type ``dashboard-plugin`` to your charm or layers ``metadata.yaml``:

```yaml
requires:
  dashboard:
    interface: dashboard-plugin
```

# Bugs

Please report bugs on [Launchpad](https://bugs.launchpad.net/openstack-charms/+filebug).

For development questions please refer to the OpenStack [Charm Guide](https://github.com/openstack/charm-guide).
