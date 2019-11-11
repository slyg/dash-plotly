RED = 'rgb(229,89,52)'
ORANGE = 'rgb(255, 140, 17)'
GREEN = 'rgb(124,206,119)'
YELLOW = 'rgb(219,210,82)'
GREY = 'rgb(204, 204, 204)'
WHITE = 'rgb(255, 255, 255)'
TRANSPARENT = 'rgba(0,0,0,0)'

colors_map = {
    'SUCCESS': GREEN,
    'ABORTED': ORANGE,
    'FAILURE': RED,
    'UNKOWN':  GREY
}

colorscale = {
    'GreenToRed': [[0, GREEN], [1, RED]],
    'GreyToRed': [[0, GREY], [1, RED]],
    'WhiteToRed': [[0, WHITE], [1, RED]],
    'OrangeToRed': [[0, ORANGE], [1, RED]],
    'YellowToRed': [[0, YELLOW], [1, RED]],
    'HueGradient': [
        [0, RED],
        [0.08333333, 'rgb(227,58,83)'],
        [0.16666667, 'rgb(225,64,145)'],
        [0.25, 'rgb(223,70,201)'],
        [0.33333333, 'rgb(190,76,221)'],
        [0.41666667, 'rgb(141,82,219)'],
        [0.5, 'rgb(97,88,218)'],
        [0.58333333, 'rgb(93,127,216)'],
        [0.66666667, 'rgb(98,172,214)'],
        [0.75, 'rgb(104,211,212)'],
        [0.83333333, 'rgb(109,210,175)'],
        [0.91666667, 'rgb(114,208,142)'],
        [1, GREEN]
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
    ]
}

graph_title_font = dict(
    size=12
)
