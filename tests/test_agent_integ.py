# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
#
# Copyright 2020, Battelle Memorial Institute.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government. Neither the United States Government nor the
# United States Department of Energy, nor Battelle, nor any of their
# employees, nor any jurisdiction or organization that has cooperated in the
# development of these materials, makes any warranty, express or
# implied, or assumes any legal liability or responsibility for the accuracy,
# completeness, or usefulness or any information, apparatus, product,
# software, or process disclosed, or represents that its use would not infringe
# privately owned rights. Reference herein to any specific commercial product,
# process, or service by trade name, trademark, manufacturer, or otherwise
# does not necessarily constitute or imply its endorsement, recommendation, or
# favoring by the United States Government or any agency thereof, or
# Battelle Memorial Institute. The views and opinions of authors expressed
# herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY operated by
# BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830
# }}}

import gevent
from pathlib import Path

from volttron.client.messaging.health import STATUS_GOOD
from volttron.client.vip.agent import Agent
from volttrontesting.platformwrapper import PlatformWrapper


def test_platform_driver_agent_successful_install_on_volttron_platform(
        publish_agent: Agent, volttron_instance: PlatformWrapper):
    # Agent install path based upon root of this repository
    agent_dir = Path(__file__).parent.parent.resolve().as_posix()
    config = {
        "driver_scrape_interval": 0.05,
        "publish_breadth_first_all": "false",
        "publish_depth_first": "false",
        "publish_breadth_first": "false"
    }
    pdriver_id = "pdriver_health_id"

    pdriver_uuid = volttron_instance.install_agent(agent_dir=agent_dir,
                                                   config_file=config,
                                                   start=False,
                                                   vip_identity=pdriver_id)

    assert pdriver_uuid is not None
    gevent.sleep(1)

    started = volttron_instance.start_agent(pdriver_uuid)
    assert started
    assert volttron_instance.is_agent_running(pdriver_uuid)

    assert publish_agent.vip.rpc.call(
        pdriver_id, "health.get_status").get(timeout=10).get('status') == STATUS_GOOD
