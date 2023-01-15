##
# @brief Simple motion detection sensor that uses the WiFi signal strength
#        signal (RSSI) to detect motions.
#
# @author Jan Peter Riegel <JanPeter1@familie-riegel.de>
# Copyright (c) 2022
##

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.components import sensor
from esphome.const import (
    CONF_TIMING,
    CONF_HYSTERESIS,
    CONF_BUFFER_SIZE,
    CONF_ID,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    ENTITY_CATEGORY_DIAGNOSTIC,
    STATE_CLASS_MEASUREMENT,
    UNIT_DECIBEL_MILLIWATT,
)

DEPENDENCIES = ["wifi"]

CONF_RSSI = "expose_rssi"
CONF_MOTION_BINARY = "expose_binary_motion_sensor"

CODEOWNERS = ["@JanPeter1", "@IdoFreeman"]

wifi_csi_ns = cg.esphome_ns.namespace("wifi_csi")
WiFiCSIComponent = wifi_csi_ns.class_("WiFiCSIComponent", cg.PollingComponent)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(WiFiCSIComponent),
        cv.Optional(CONF_RSSI): sensor.sensor_schema(
            unit_of_measurement=UNIT_DECIBEL_MILLIWATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
            state_class=STATE_CLASS_MEASUREMENT,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        cv.Optional(CONF_MOTION_BINARY): binary_sensor.binary_sensor_schema(
            WiFiCSIComponent
        ).extend(
            {
                cv.Optional(CONF_TIMING): cv.positive_time_period_milliseconds,
                cv.Optional(CONF_HYSTERESIS): cv.float_,
                cv.Optional(CONF_BUFFER_SIZE): cv.int_,
            }
        ),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])

    await cg.register_component(var, config)
    # await binary_sensor.new_binary_sensor(var, config)
    if CONF_MOTION_BINARY in config:
        bin_sens = await binary_sensor.new_binary_sensor(config[CONF_MOTION_BINARY])
        cg.add(var.set_binary_motion_sensor(bin_sens))

        if CONF_TIMING in config:
            cg.add(var.set_timing(config[CONF_TIMING]))
        if CONF_HYSTERESIS in config:
            cg.add(var.set_sensitivity(config[CONF_HYSTERESIS]))
        if CONF_BUFFER_SIZE in config:
            cg.add(var.set_buffer_size(config[CONF_BUFFER_SIZE]))

    if CONF_RSSI in config:
        rssi_sens = await sensor.new_sensor(config[CONF_RSSI])
        cg.add(var.set_expose_rssi(rssi_sens))
