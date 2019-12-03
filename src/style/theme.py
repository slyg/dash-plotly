govuk_colour = {
    "red": 'rgb(212,53,28)',
    "yellow": 'rgb(255,221,0)',
    "green": 'rgb(0,112,60)',
    "light-green": 'rgb(133,153,75)',
    "dark-blue": 'rgb(0,48,120)',
    "blue": 'rgb(29,112,184)',
    "light-blue": 'rgb(86,148,202)',
    "purple": 'rgb(76,44,146)',
    "light-purple": 'rgb(111,114,175)',
    "bright-purple": 'rgb(145,43,136)',
    "light-pink": 'rgb(244,153,190)',
    "pink": 'rgb(213,56,128)',
    "orange": 'rgb(244,119,56)',
    "brown": 'rgb(181,136,64)',
    "turquoise": 'rgb(40,161,151)',
    "black": 'rgb(11,12,12)',
    "dark-grey": 'rgb(98,106,110)',
    "mid-grey": 'rgb(177,180,182)',
    "light-grey": 'rgb(243,242,241)',
    "white": 'rgb(255,255,255)',
}

# Commonly used colors

RED = govuk_colour['red']
ORANGE = govuk_colour['orange']
GREEN = govuk_colour['light-green']
YELLOW = govuk_colour['yellow']
BLUE = govuk_colour['light-blue']
PURPLE = govuk_colour['purple']
GREY = govuk_colour['mid-grey']
LIGHT_GREY = govuk_colour['light-grey']
WHITE = govuk_colour['white']
WHITE_ALPHA_8 = 'rgba(255, 255, 255, 0.8)'
BLACK = govuk_colour['black']
TRANSPARENT = 'rgba(0,0,0,0)'

BRAND = 'rgb(76, 44, 146)'  # HMCTS primary color


colors_map = {
    'SUCCESS': GREEN,
    'ABORTED': ORANGE,
    'FAILURE': RED,
    'UNKOWN':  GREY
}

colorway = {
    'GovUkColours': [
        govuk_colour['green'],
        govuk_colour['dark-blue'],
        govuk_colour['blue'],
        govuk_colour['light-blue'],
        govuk_colour['purple'],
        govuk_colour['light-purple'],
        govuk_colour['bright-purple'],
        govuk_colour['pink'],
        govuk_colour['light-pink'],
        govuk_colour['orange'],
        govuk_colour['brown'],
        govuk_colour['light-green'],
        govuk_colour['turquoise'],
    ][::-1],
    'BadToGood': [
        govuk_colour['red'],
        govuk_colour['light-purple'],
        govuk_colour['light-blue'],
    ],
}

colorscale = {
    'GreenToRed': [[0, GREEN], [1, RED]],
    'GreyToRed': [[0, GREY], [1, RED]],
    'WhiteToRed': [[0, WHITE], [1, RED]],
    'OrangeToRed': [[0, ORANGE], [1, RED]],
    'YellowToRed': [[0, YELLOW], [1, RED]],
    'HueGradient': [
        [0, GREEN],
        [0.7, YELLOW],
        [0.85, ORANGE],
        [1, RED],
    ],
    'NegativelyOriented': [
        [0, GREEN],
        [0.08333333, YELLOW],
        [1, RED],
    ],
    'WhiteIfNoData': [
        [0, WHITE],
        [0.00000001, TRANSPARENT],
        [1, TRANSPARENT]
    ],
    'Rainbow': [
        [0, GREY],
        [0.25, BLUE],
        [0.33, GREEN],
        [0.50, YELLOW],
        [0.66, ORANGE],
        [0.75, RED],
        [1, govuk_colour["bright-purple"]],
    ],
}

graph_title_font = dict(
    family='GDS Transport,Arial,sans-serif',
    size=14,
    color=BLACK,
)

pie_line_style = dict(color=WHITE, width=2)
