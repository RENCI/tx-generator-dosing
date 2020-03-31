import requests

json_headers = {
    "Accept": "application/json"
}

json_post_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

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

generator_input = {
    "dose": 180,
    "tau": 12,
    "crcl": 50,
    "t_infusion": 6,
    "vd": 22.59,
    "num_cycles": 4
}

generator_output = {
    "parameters": {
        "crcl": 50,
        "dose": 180,
        "group": "guidance",
        "peak": 5.988275788802068,
        "tau": 12,
        "trough": 2.2859999017896673
    },
    'data': [{
        "x": 0,
        "y": 0,
        "group": "guidance"
        },
        {
        "x": 6,
        "y": 5.115358321074912,
        "group": "guidance"
        },
        {
        "x": 12,
        "y": 1.9527672124692657,
        "group": "guidance"
        },
        {
        "x": 18,
        "y": 5.860819253965945,
        "group": "guidance"
        },
        {
        "x": 24,
        "y": 2.2373438885407997,
        "group": "guidance"
        },
        {
        "x": 30,
        "y": 5.969455241434752,
        "group": "guidance"
        },
        {
        "x": 36,
        "y": 2.2788152344579182,
        "group": "guidance"
        },
        {
        "x": 42,
        "y": 5.985286758892745,
        "group": "guidance"
    }]
}


def test_concentration_data():
    resp = requests.post("http://tx-generator-dosing:8080/concentration_data", headers=json_post_headers,
                         json=generator_input)

    assert resp.status_code == 200
    output = resp.json()
    assert output == generator_output


def test_config():
    resp = requests.get("http://tx-generator-dosing:8080/config", headers=json_headers)

    assert resp.status_code == 200
    assert resp.json() == config


def test_ui():
    resp = requests.get("http://tx-generator-dosing:8080/ui")

    assert resp.status_code == 200
