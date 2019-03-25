from ..exercise_converter.helper.ChangeSorterMarkup import *
from ..exercise_converter.helper.WidgetRenderer import *
from nose.tools import assert_equal


def test_render_sorting_widget_1():
    input_values = SorterWidget(nr=1,
                                columna='ColA',
                                columnb='ColB',
                                matches=[SorterWidgetMatch(columna='A', columnb='A'),
                                         SorterWidgetMatch(columna='B', columnb='B')])
    expected_output =  """
"sorting_widget1": {
  "type": "sorter",
  "properties": {
    "values": [
      [
        {
          "value": "A"
        },
        {
          "value": "A"
        }
      ],
      [
        {
          "value": "B"
        },
        {
          "value": "B"
        }
      ]
    ],
    "columnnamea": "ColA",
    "columnnameb": "ColB"
  },
  "name": "sorting_widget1"
}
"""

    actual_output = render_sorting_widget(input_values)
    assert_equal(expected_output, actual_output)


def test_render_sorting_widget_2():
    input_values = SorterWidget(nr=2,
                                columna='ColumnA',
                                columnb='ColumnB',
                                matches=[SorterWidgetMatch(columna='A', columnb='A'),
                                         SorterWidgetMatch(columna='B', columnb='B')])
    expected_output =  """
"sorting_widget2": {
  "type": "sorter",
  "properties": {
    "values": [
      [
        {
          "value": "A"
        },
        {
          "value": "A"
        }
      ],
      [
        {
          "value": "B"
        },
        {
          "value": "B"
        }
      ]
    ],
    "columnnamea": "ColumnA",
    "columnnameb": "ColumnB"
  },
  "name": "sorting_widget2"
}
"""

    actual_output = render_sorting_widget(input_values)
    assert_equal(expected_output, actual_output)


def test_render_sorting_widget_3():
    input_values = SorterWidget(nr=2,
                                columna='ColumnA',
                                columnb='ColumnB',
                                matches=[SorterWidgetMatch(columna='AA', columnb='AAA'),
                                         SorterWidgetMatch(columna='BB', columnb='BBB')])
    expected_output =  """
"sorting_widget2": {
  "type": "sorter",
  "properties": {
    "values": [
      [
        {
          "value": "AA"
        },
        {
          "value": "AAA"
        }
      ],
      [
        {
          "value": "BB"
        },
        {
          "value": "BBB"
        }
      ]
    ],
    "columnnamea": "ColumnA",
    "columnnameb": "ColumnB"
  },
  "name": "sorting_widget2"
}
"""

    actual_output = render_sorting_widget(input_values)
    assert_equal(expected_output, actual_output)


def test_render_sorting_widget_4():
    input_values = SorterWidget(nr=2,
                                columna='ColumnA',
                                columnb='ColumnB',
                                matches=[SorterWidgetMatch(columna='AA', columnb='AAA'),
                                         SorterWidgetMatch(columna='CC', columnb='CCC'),
                                         SorterWidgetMatch(columna='BB', columnb='BBB')])
    expected_output =  """
"sorting_widget2": {
  "type": "sorter",
  "properties": {
    "values": [
      [
        {
          "value": "AA"
        },
        {
          "value": "AAA"
        }
      ],
      [
        {
          "value": "CC"
        },
        {
          "value": "CCC"
        }
      ],
      [
        {
          "value": "BB"
        },
        {
          "value": "BBB"
        }
      ]
    ],
    "columnnamea": "ColumnA",
    "columnnameb": "ColumnB"
  },
  "name": "sorting_widget2"
}
"""

    actual_output = render_sorting_widget(input_values)
    assert_equal(expected_output, actual_output)
