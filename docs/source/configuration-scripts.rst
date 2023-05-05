# TODO: This needs cleaned up. "Old style" is almost certainly irrelevant at this point, but the install script
#  is still useful.
# TODO: This is not currently linked by the documentation as the scripts have not yet been ported.

Converting Old Style Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The new Platform Driver no longer supports the old style of device configuration.  The old `device_list` setting is
ignored.

To simplify updating to the new format, `scripts/update_platform_driver_config.py` is provided to automatically update to
the new configuration format.

With the platform running run:

.. code-block:: bash

    python scripts/update_platform_driver_config.py <old configuration> <output>

`old_configuration` is the main configuration file in the old format. The script automatically modifies the driver
files to create references to CSV files and adds the CSV files with the appropriate name.

`output` is the target output directory.

If the ``--keep-old`` switch is used, the old configurations in the output directory (if any) will not be deleted before
new configurations are created.  Matching names will still be overwritten.

The output from `scripts/update_platform_driver_config.py` can be automatically added to the configuration store
for the Platform Driver agent with `scripts/install_platform_driver_configs.py`.

Creating and naming configuration files in the form needed by `scripts/install_platform_driver_configs.py` can speed up
the process of changing and updating a large number of configurations. See the ``--help`` message for
`scripts/install_platform_driver_configs.py` for more details.

