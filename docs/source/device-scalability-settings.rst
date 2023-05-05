.. _Device-Scalability-Settings:

To improve the scalability of the platform, unneeded device state publishes for a device can be turned off.
All of the following setting are optional and will override the value set in the main platform driver configuration.

    - **publish_depth_first_all** - Enable "depth first" publish of all points to a single topic.
    - **publish_breadth_first_all** - Enable "breadth first" publish of all points to a single topic.
    - **publish_depth_first** - Enable "depth first" device state publishes for each point on the device.
    - **publish_breadth_first** - Enable "breadth first" device state publishes for each point on the device.

By default, the ``publish_breadth_first_all``, ``publish_depth_first``, and
``publish_breadth_first`` are set to to ``False`` unless they are specifically needed by an agent running on
the platform.


.. note::

    All Historian Agents require ``publish_depth_first_all`` to be set to ``True`` in order to capture data.

By default, the value of each point on a device is published 4 different ways when the device state is published.
Consider the following settings in a driver configuration stored under the name ``devices/pnnl/isb1/vav1``:

.. code-block:: json

    {
        "driver_config": {"device_address": "10.1.1.5",
                          "device_id": 500},

        "driver_type": "bacnet",
        "registry_config":"config://registry_configs/vav.csv",
    }

In the `vav.csv` file, a point has the name `temperature`.  For these examples the current value of the
point on the device happens to be 75.2 and the meta data is

.. code-block:: json

    {"units": "F"}

When the driver publishes the device state the following two things will be published for this point:

    A "depth first" publish to the topic `devices/pnnl/isb1/vav1/temperature` with the following message:

        .. code-block:: python

            [75.2, {"units": "F"}]

    A "breadth first" publish to the topic `devices/temperature/vav1/isb1/pnnl` with the following message:

        .. code-block:: python

            [75.2, {"units": "F"}]

    These publishes can be turned off by setting `publish_depth_first` and `publish_breadth_first` to `false`
    respectively.

Also these two publishes happen once for all points:

    A "depth first" publish to the topic `devices/pnnl/isb1/vav1/all` with the following message:

        .. code-block:: python

            [{"temperature": 75.2, ...}, {"temperature":{"units": "F"}, ...}]

    A "breadth first" publish to the topic `devices/all/vav1/isb1/pnnl` with the following message:

        .. code-block:: python

            [{"temperature": 75.2, ...}, {"temperature":{"units": "F"}, ...}]

    These publishes can be turned off by setting `publish_depth_first_all` and `publish_breadth_first_all` to
    ``false`` respectively.
