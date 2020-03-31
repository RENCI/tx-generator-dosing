import math

config = {
    "title": "Dosing concentration graph data generator",
    "piid": "tx-generator-dosing",
    "pluginType": "c",
    "pluginParameters": {
        "legalParameters": [ {
            "value_type": "number",
            "name": "dose"
        },
        {
            "value_type": "number",
            "name": "tau"
        },
        {
          "value_type": "number",
          "name": "crcl"
        },
        {
          "value_type": "number",
          "name": "t_infusion"
        },
        {
          "value_type": "number",
          "name": "vd"
        },
        {
          "value_type": "integer",
          "name": "num_cycles"
        } ]
    }
}


def get_config():
    return config


def get_concentration_data(body):
    dose = float(body['dose'])
    tau = float(body['tau'])
    crcl = float(body['crcl'])
    t_infusion = float(body.get('t_infusion', 0.5))
    vd = float(body.get('vd', 22.59))
    n = int(body.get('num_cycles', 4))
    group = body.get('group', 'guidance')

    kel = 0.00293*crcl+0.014

    # Estimated peak/trough convergence
    peak_end = dose * (1 - math.exp(-kel * t_infusion)) / (t_infusion * vd * kel * (1 - math.exp(-kel * tau)))
    trough_end = peak_end * math.exp(-kel * (tau - t_infusion))

    peak0 = dose / vd
    peak = 0

    output_data = {
        'parameters': {
            'dose': dose,
            'crcl': crcl,
            'tau': tau,
            'peak': peak_end,
            'trough': trough_end,
            'group': group
        },
        'data': [{
            'x': 0,
            'y': 0,
            'group': group
        }]
    }

    x = t_infusion
    max_x = tau * n
    data = output_data['data']
    while x < max_x:
        m = (x - t_infusion) % tau
        if m == 0:
            # Simulate infusion
            steps = 10000
            y = data[len(data) - 1]['y']
            k1 = peak0 / steps
            k2 = math.exp(-kel * t_infusion / steps)
            for i in range(1, steps+1):
                y = (y + k1) * k2
            peak = y

        y = peak * math.exp(-kel * m)

        data.append({
            'x': x,
            'y': y,
            'group': group
        })
        x += t_infusion

    return output_data
