
pre_command = ['charger switch on', 'ft temperature read', 'adc enable 1', 'adc read ibat', 'adc read vbat',
               'syscfg print SrNm', 'ft auto ship disable']
loop_command = ['audio play findmy', 'audio stop', 'batman data']
post_command = ['ft version', 'ft auto ship enable']

wait_command = {'ft version': 1, 'audio play findmy': 62}
