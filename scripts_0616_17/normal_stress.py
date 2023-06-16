
pre_command = ['charger switch on', 'ft temperature read', 'adc enable 1', 'adc read ibat', 'adc read vbat',
               'syscfg print SrNm', 'ft auto ship disable', 'bud state both disable',
               'buckboost enable out', 'locust_mgr pp left enable', 'locust_mgr pp right enable',
               'locust_mgr pullup left enable', 'locust_mgr pullup right enable', 'ft tunnel open left finite',
               'syscfg print SrNm', 'ft uvp disable', 'upy test rel_hs_rf_pink', 'ft tunnel open right finite',
               'syscfg print SrNm', 'ft uvp disable', 'upy test rel_hs_rf_pink']

loop_command = ['audio play findmy', 'audio stop', 'batman data', 'bud status', 'locust_mgr pp left disable ',
                'locust_mgr pullup left enable', 'locust_mgr pp left enable', 'locust_mgr pullup left enable',
                'bud status', 'locust_mgr pp right disable', 'locust_mgr pullup right enable',
                'locust_mgr pp right enable', 'locust_mgr pullup right enable']

post_command = ['bud state both disable', 'buckboost enable out', 'locust_mgr pp left enable',
                'locust_mgr pp right enable', 'locust_mgr pullup left enable', 'locust_mgr pullup right enable',
                'ft tunnel open left finite', 'ft version', 'ft uvp enable', 'ft reset', 'ft tunnel open right finite',
                'ft version', 'ft uvp enable', 'ft reset', 'ft version', 'ft auto ship enable']

wait_command = {'ft reset': 20, 'upy test rel_hs_rf_pink': 20, 'ft tunnel open right finite': 2,
                'ft tunnel open left finite': 2, 'audio play findmy': 62, 'bud status': 4}
