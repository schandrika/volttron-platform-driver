"""Unit tests for agent"""


def test_derive_device_topic_should_succeed(platform_driver):
    config_name = "mytopic/foobar_topic"
    expected = "foobar_topic"

    actual = platform_driver.derive_device_topic(config_name)

    assert actual == expected


def test_stop_driver_should_return_none_on_empty_drivers(platform_driver):
    device_topic = "mytopic/foobar_topic"

    actual = platform_driver.stop_driver(device_topic)

    assert actual is None


def test_scrape_starting_should_return_none_on_false_scalability_test(platform_driver):
    device_topic = "mytopic/foobar_topic"

    actual = platform_driver.scrape_starting(device_topic)

    assert actual is None
