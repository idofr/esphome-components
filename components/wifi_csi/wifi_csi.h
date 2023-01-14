
/**
 * @brief Simple motion detection sensor that uses the WiFi signal strength
 *        signal (RSSI) to detect motions.
 *
 * @author Jan Peter Riegel <JanPeter1@familie-riegel.de>
 * Copyright (c) 2022
 */

#pragma once

#include "esphome.h"
#include "esphome/core/log.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/wifi/wifi_component.h"
#ifdef USE_ESP32
#include <WiFi.h>
#endif

#ifdef USE_ESP8266
#include <ESP8266WiFi.h>
#endif

namespace esphome
{
    namespace wifi_csi
    {

        // detect motion when the RSSI value from the WiFi reception deviates from the average
        // value. Inspired by: https://gist.github.com/jaretburkett/b2779bd7bf19b0a8e025
        class CsiSensor : public PollingComponent, public binary_sensor::BinarySensor
        {
        public:
            CsiSensor();
            ~CsiSensor();

            float get_setup_priority() const override;
            void dump_config();

            void set_timing(int pollingInterval);
            void set_sensitivity(float sensitivity);
            void set_buffer_size(int bufferSize);
            void set_expose_rssi(bool exposeRssi);

            void update() override;

        protected:
            // config vars:
            int m_pollingInterval; ///< polling interval in ms (default: 100)
            int m_bufferSize;      ///< size of the buffer (default: 100)
            float m_sensitivity;   ///< sensitivity - deviation from average more than this will trigger a motion (default: 2)
            bool m_expose_rssi;     ////< setting this to True in the ESPHome config will create a sensor with the actual RSSI value
            
            // class vars
            int *m_rssi;           ///< buffer of rssi values
        };

    } // namespace wifi_csi
} // namespace esphome
