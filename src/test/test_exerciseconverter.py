from ..exercise_converter.helper.exerciseconverterfunctions import *
from nose.tools import assert_equal



def test_change_part_of_markup_1():
    input_values = ['$x^2$\n']
    expected_output = ['[[eql x^2]]\n']
    output = list(change_part_of_markup(input_values))
    assert_equal(expected_output, output)


def test_change_part_of_markup_2():
    input_values = ['$x^2$ test $y \\cdot x$\n']
    expected_output = ['[[eql x^2]] test [[eql y \\cdot x]]\n']
    output = list(change_part_of_markup(input_values))
    assert_equal(expected_output, output)


def test_change_part_of_markup_3():
    input_values = '''\\[x^2\\]'''
    expected_output = ['[[eq x^2]]']
    output = list(change_part_of_markup(input_values.split('\n')))
    assert_equal(expected_output, output)


def test_change_part_of_markup_4():
    input_values = ["Bestem $f'(x)$ og $g'(x)$.\n", '\\[\n', "f'(x) = \\frac{1}{\\sqrt{1 - x^ 2}} \\qquad g'(x) = 2/3\n", '\\]\n']
    expected_output = ["Bestem [[eql f'(x)]] og [[eql g'(x)]].\n", '[[eq \n', "f'(x) = \\frac{1}{\\sqrt{1 - x^ 2}} \\qquad g'(x) = 2/3\n", ']]\n']
    output = list(change_part_of_markup(input_values))
    assert_equal(expected_output, output)


def test_change_part_of_markup_5():
    input_values = ['$g(x)$\n', '\\[\n', 'f\n', '\\]\n']
    expected_output = ["[[eql g(x)]]\n", '[[eq \n', "f\n", ']]\n']
    output = list(change_part_of_markup(input_values))
    assert_equal(expected_output, output)


def test_change_part_of_markup_6():
    input_values = ["Bestem $f'(x)$ og $g'(x)$.\n", '\\begin{align*}\n', "f'(x) = \\frac{1}{\\sqrt{1 - x^ 2}} \\qquad g'(x) = 2/3\n", '\\end{align*}\n']
    expected_output = ["Bestem [[eql f'(x)]] og [[eql g'(x)]].\n", '[[eq \n', "f'(x) = \\frac{1}{\\sqrt{1 - x^ 2}} \\qquad g'(x) = 2/3\n", ']]\n']
    output = list(change_part_of_markup(input_values))
    assert_equal(expected_output, output)


def test_change_part_of_markup_7():
    input_values = ["Bestem \\(f'(x)\\) og \\(g'(x)\\).\n", '\\begin{align*}\n', "f'(x) = \\frac{1}{\\sqrt{1 - x^ 2}} \\qquad g'(x) = 2/3\n", '\\end{align*}\n']
    expected_output = ["Bestem [[eql f'(x)]] og [[eql g'(x)]].\n", '[[eq \n', "f'(x) = \\frac{1}{\\sqrt{1 - x^ 2}} \\qquad g'(x) = 2/3\n", ']]\n']
    output = list(change_part_of_markup(input_values))
    assert_equal(expected_output, output)


def test_change_part_of_markup_8():
    input_values = [r"vis \underline{dette} en gang til"]
    expected_output = ['vis **dette** en gang til']
    output = list(change_part_of_markup(input_values))
    assert_equal(expected_output, output)


def test_change_part_of_markup_9():
    input_values = [r"vis \emph{dette} en gang til"]
    expected_output = ['vis *dette* en gang til']
    output = list(change_part_of_markup(input_values))
    assert_equal(expected_output, output)


def test_change_multi_choice_markup_1():
    input_values = ["\\begin{multichoice}[randomizeorder, selectmultiple]\n", "\\itemtrue ja\n", "\\itemfalse nej\n", "\\end{multichoice}\n"]
    expected_output = ["[[ref multi_choice1]]\n"]
    temp = ChangeMultiChoiceMarkup()
    output = list(temp.generator(input_values))
    assert_equal(expected_output, output)
    detected_environments = [MultiChoice(nr=1,
                                         items=[MultiChoiceItem(text='ja', is_correct_answer='true'),
                                                MultiChoiceItem(text='nej', is_correct_answer='false')],
                                         parameters=['randomizeorder', 'selectmultiple'])]
    assert_equal(detected_environments, temp.detected_multi_choice_markups)


def test_change_multi_choice_markup_2():
    input_values = ["\\begin{multichoice}[randomizeorder, selectmultiple]\n", "\\itemtrue ja\n", "\\itemfalse nej\n", "\\end{multichoice}\n", "\\begin{multichoice}\n", "\\itemtrue ja\n", "\\end{multichoice}\n"]
    expected_output = ["[[ref multi_choice1]]\n", "[[ref multi_choice2]]\n"]
    temp = ChangeMultiChoiceMarkup()
    output = list(temp.generator(input_values))
    assert_equal(expected_output, output)
    detected_environments = [MultiChoice(nr=1,
                                         items=[MultiChoiceItem(text='ja', is_correct_answer='true'),
                                                MultiChoiceItem(text='nej', is_correct_answer='false')],
                                         parameters=['randomizeorder', 'selectmultiple']),
                             MultiChoice(nr=2,
                                         items=[MultiChoiceItem(text='ja', is_correct_answer='true')],
                                         parameters=[])]
    assert_equal(detected_environments, temp.detected_multi_choice_markups)


def test_change_sorter_markup_1():
    input_values = ["\\begin{sortingwidget}{a}{b}\n", "A&a\n", "B&b\n", "\\end{sortingwidget}\n"]
    expected_output = ["[[ref sorting_widget1]]\n"]
    temp = ChangeSorterMarkup()
    output = list(temp.generator(input_values))
    assert_equal(expected_output, output)
    detected_environments = [SorterWidget(nr=1,
                                          columna='a',
                                          columnb='b',
                                          matches=[SorterWidgetMatch(columna='A', columnb='a'),
                                                   SorterWidgetMatch(columna='B', columnb='b')])]
    assert_equal(detected_environments, temp.detected_sorting_widgets_markups)


def test_change_answermatrix_markup_1():
    input_values = ["\\begin{answermatrix}\n", "1\n", "\\end{answermatrix}\n"]
    expected_output = ["[[ref answermatrix1]]\n"]
    temp = ChangeAnswerMatrixMarkup()
    output = list(temp.generator(input_values))
    assert_equal(expected_output, output)
    detected_environments = [AnswerMatrix(nr=1,
                                          number_of_rows=1,
                                          number_of_columns=1,
                                          items=[AnswerMatrixRow(rownr=1,
                                                                 nelements=1,
                                                                 elements=[AnswerMatrixRowElement(1, '1')])
                                                ]
                                          )
                             ]
    assert_equal(detected_environments, temp.detected_answer_matrix_markups)


def test_change_answermatrix_markup_2():
    input_values = ["\\begin{answermatrix}\n", "1 & 2 & 4 \\\\\n", "3 & 5 & 4", "\\end{answermatrix}\n"]
    expected_output = ["[[ref answermatrix1]]\n"]
    temp = ChangeAnswerMatrixMarkup()
    output = list(temp.generator(input_values))
    assert_equal(expected_output, output)
    detected_environments = [AnswerMatrix(nr=1,
                                          number_of_rows=2,
                                          number_of_columns=3,
                                          items=[AnswerMatrixRow(rownr=1,
                                                                 nelements=3,
                                                                 elements=[AnswerMatrixRowElement(1, '1'),
                                                                           AnswerMatrixRowElement(2, '2'),
                                                                           AnswerMatrixRowElement(3, '4')]),
                                                 AnswerMatrixRow(rownr=2,
                                                                 nelements=3,
                                                                 elements=[AnswerMatrixRowElement(1, '3'),
                                                                           AnswerMatrixRowElement(2, '5'),
                                                                           AnswerMatrixRowElement(3, '4')])
                                                ]
                                          )
                             ]
    assert_equal(detected_environments, temp.detected_answer_matrix_markups)


def test_change_answermatrix_markup_3():
    input_values = [" \\begin{answermatrix}\n", "1 & 2 & 4 \\\\\n", "3 & 5 & 4", "  \\end{answermatrix}\n"]
    expected_output = ["[[ref answermatrix1]]\n"]
    temp = ChangeAnswerMatrixMarkup()
    output = list(temp.generator(input_values))
    assert_equal(expected_output, output)
    detected_environments = [AnswerMatrix(nr=1,
                                          number_of_rows=2,
                                          number_of_columns=3,
                                          items=[AnswerMatrixRow(rownr=1,
                                                                 nelements=3,
                                                                 elements=[AnswerMatrixRowElement(1, '1'),
                                                                           AnswerMatrixRowElement(2, '2'),
                                                                           AnswerMatrixRowElement(3, '4')]),
                                                 AnswerMatrixRow(rownr=2,
                                                                 nelements=3,
                                                                 elements=[AnswerMatrixRowElement(1, '3'),
                                                                           AnswerMatrixRowElement(2, '5'),
                                                                           AnswerMatrixRowElement(3, '4')])
                                                ]
                                          )
                             ]
    assert_equal(detected_environments, temp.detected_answer_matrix_markups)


def test_get_exercises_1():
    input_values = '''\\begin{exercise}{Name}\nLine\n\\end{exercise}'''
    expected_output = [Exercise(name = 'Name', content = ['Line'])]
    output = list(get_exercises(input_values.split('\n')))
    assert_equal(expected_output, output)


def test_get_exercises_2():
    input_values = '''\\begin{exercise}{Name}\n% Comment\nLine\n\\end{exercise}'''
    expected_output = [Exercise(name = 'Name', content = ['Line'])]
    output = list(get_exercises(input_values.split('\n')))
    assert_equal(expected_output, output)


def test_get_exercises_3():
    input_values = ''' \\begin{exercise}{NameWithÆØÅæøå}\n% Comment\nLine\n\\end{exercise}'''
    expected_output = [Exercise(name = 'NameWithÆØÅæøå', content = ['Line'])]
    output = list(get_exercises(input_values.split('\n')))
    assert_equal(expected_output, output)


def test_change_answer_box_markup_1():
    input_values = '''Question\n\\answerbox{2}\n\\hint\nHints'''
    expected_output = 'Question\n[[ref input1]]\n\n\\hint\nHints'
    temp = ChangeAnswerBoxMarkup()
    output = "\n".join(list(temp.generator(input_values.split('\n'))))
    assert_equal(expected_output, output)
    detected_environments = [Answer(nr=1, content='2')]
    assert_equal(detected_environments, list(temp.get_answers()))


def test_change_answer_box_markup_2():
    input_values = ''
    expected_output = ''
    temp = ChangeAnswerBoxMarkup()
    output = "\n".join(list(temp.generator(input_values.split('\n'))))
    assert_equal(expected_output, output)
    detected_environments = []
    assert_equal(detected_environments, list(temp.get_answers()))


def test_change_answer_box_markup_3():
    input_values = "Line 1\n\\answerbox{test}\n"
    expected_output = "Line 1\n[[ref input1]]\n\n"
    temp = ChangeAnswerBoxMarkup()
    output = "\n".join(list(temp.generator(input_values.split('\n'))))
    assert_equal(expected_output, output)
    detected_environments = [Answer(1, "test")]
    assert_equal(detected_environments, list(temp.get_answers()))


def test_change_answer_box_markup_4():
    input_values = "Line 1\n\\answerbox{test one}\nLine 3\n\\answerbox{test two}\n"
    temp = ChangeAnswerBoxMarkup()
    for line in temp.generator(input_values.split('\n')):
        pass
    detected_environments = [Answer(1, "test one"), Answer(2, "test two")]
    assert_equal(detected_environments, list(temp.get_answers()))


def test_change_answer_box_markup_5():
    input_values = "Line 1 \\answerbox{test one}\nLine 3 \\answerbox{test two}\n"
    temp = ChangeAnswerBoxMarkup()
    for line in temp.generator(input_values.split('\n')):
        pass
    detected_environments = [Answer(1, "test one"), Answer(2, "test two")]
    assert_equal(detected_environments, list(temp.get_answers()))


def test_change_hint_markup_1():
    input_values = '''Line 1 \n\\hint\nLine 2'''
    temp = ChangeHintMarkup()
    temp.parser(input_values.split('\n'))
    expected_output = [Hint(nr = 1, content = 'Line 2')]
    output = list(temp.get_hints())
    assert_equal(expected_output, output)


def test_add_extra_backslashes_1():
    input_values = ["line with no markup"]
    output = ["line with no markup"]
    assert_equal(output, list(add_extra_backslashes(input_values)))


def test_add_extra_backslashes_2():
    input_values = ["line with no \\ markup"]
    output = ["line with no \\\\ markup"]
    assert_equal(output, list(add_extra_backslashes(input_values)))


def test_full_example_1():
    input_values = r"""\newpage

\begin{exercise}{Differentiering 1-1}
% Test comment.

Bestem $\frac{d}{dx} x^2$.

\answerbox{2x}

\hint

Benyt formlen
\[
\frac{d}{dx} x^n = n \cdot x^{n - 1}
\]

\hint

Sæt $n = 2$
\[
\frac{d}{dx} x^2 = 2 \cdot x^{2 - 1} = 2 x
\]

\end{exercise}


"""
    expected_output = r"""
{
  "name": "Differentiering 1-1",
  "document": "Bestem [[eql \\frac{d}{dx} x^2]].\n[[ref input1]]\n\n\n \n\n[[ref hint1]] \n\n[[ref hint2]] ",
  "widgets": {
    "input1": {
      "type": "equation-input",
      "properties": {
        "content": "2x"
      },
      "name": "input1"
    },
    "hint1": {
      "type": "hint",
      "properties": {
        "content": "Benyt formlen\n[[eq \n\\frac{d}{dx} x^n = n \\cdot x^{n - 1}\n]]"
      },
      "name": "hint1"
    },
    "hint2": {
      "type": "hint",
      "properties": {
        "content": "Sæt [[eql n = 2]]\n[[eq \n\\frac{d}{dx} x^2 = 2 \\cdot x^{2 - 1} = 2 x\n]]"
      },
      "name": "hint2"
    }
  }
}"""
    for exercise in get_exercises(change_part_of_markup(input_values.splitlines())):
        rendered_exercise = render_exercise(exercise)
        assert_equal(expected_output, rendered_exercise)
        return
    assert False


def test_full_example_2():
    input_values = r"""
\begin{exercise}{Differentiering 1-3}
Bestem $\frac{d}{dx} \left( x \cdot \sin(x) \right)$.

\answerbox{\sin(x) + x \cdot \cos(x)}

\hint
Benyt produkt reglen
\[
\frac{d}{dx} \left( f(x) \cdot g(x) \right) = \frac{d}{dx} \left( f(x) \right) \cdot g(x) + f(x) \cdot \frac{d}{dx} \left( g(x) \right)
\]

\hint
Sæt $f(x) = x$ og $g(x) = \sin(x)$
\[
\frac{d}{dx} \left( x \cdot \sin(x) \right) = \frac{d}{dx} \left( x \right) \cdot \sin(x) + x \cdot \frac{d}{dx} \left( \sin(x) \right)
\]

\hint
Differentier delled.
\[
\frac{d}{dx} \left( x \cdot \sin(x) \right) = 1 \cdot \sin(x) + x \cdot \cos(x)
\]

\hint
Der forenkles til
\[
\sin(x) + x \cdot \cos(x)
\]

\end{exercise}




"""
    expected_output = r"""
{
  "name": "Differentiering 1-3",
  "document": "Bestem [[eql \\frac{d}{dx} \\left( x \\cdot \\sin(x) \\right)]].\n[[ref input1]]\n\n\n \n\n[[ref hint1]] \n\n[[ref hint2]] \n\n[[ref hint3]] \n\n[[ref hint4]] ",
  "widgets": {
    "input1": {
      "type": "equation-input",
      "properties": {
        "content": "\\sin(x) + x \\cdot \\cos(x)"
      },
      "name": "input1"
    },
    "hint1": {
      "type": "hint",
      "properties": {
        "content": "Benyt produkt reglen\n[[eq \n\\frac{d}{dx} \\left( f(x) \\cdot g(x) \\right) = \\frac{d}{dx} \\left( f(x) \\right) \\cdot g(x) + f(x) \\cdot \\frac{d}{dx} \\left( g(x) \\right)\n]]"
      },
      "name": "hint1"
    },
    "hint2": {
      "type": "hint",
      "properties": {
        "content": "Sæt [[eql f(x) = x]] og [[eql g(x) = \\sin(x)]]\n[[eq \n\\frac{d}{dx} \\left( x \\cdot \\sin(x) \\right) = \\frac{d}{dx} \\left( x \\right) \\cdot \\sin(x) + x \\cdot \\frac{d}{dx} \\left( \\sin(x) \\right)\n]]"
      },
      "name": "hint2"
    },
    "hint3": {
      "type": "hint",
      "properties": {
        "content": "Differentier delled.\n[[eq \n\\frac{d}{dx} \\left( x \\cdot \\sin(x) \\right) = 1 \\cdot \\sin(x) + x \\cdot \\cos(x)\n]]"
      },
      "name": "hint3"
    },
    "hint4": {
      "type": "hint",
      "properties": {
        "content": "Der forenkles til\n[[eq \n\\sin(x) + x \\cdot \\cos(x)\n]]"
      },
      "name": "hint4"
    }
  }
}"""
    for exercise in get_exercises(change_part_of_markup(input_values.splitlines())):
        rendered_exercise = render_exercise(exercise)
        assert_equal(expected_output, rendered_exercise)
        return
    assert False


def test_full_example_3():
    input_values = r"""
\begin{exercise}{Linearisering 6}

	Lineariser nedenstående funktion omkring punktet $x = 5$.
	\[
	\sqrt{9-x}
	\]

	\answerbox{\frac{13 - x}{4}}

	\hint
	Lineariseringen af en funktion $f(x)$
	omkring punktet $x_0$ er givet ved
	\[
	f(x_0) + f'(x_0) \cdot (x - x_0)
	\]

\end{exercise}




"""
    expected_output = r"""
{
  "name": "Linearisering 6",
  "document": " Lineariser nedenstående funktion omkring punktet [[eql x = 5]].\n [[eq  \\sqrt{9-x} ]] [[ref input1]]\n\n\n \n\n[[ref hint1]] ",
  "widgets": {
    "input1": {
      "type": "equation-input",
      "properties": {
        "content": "\\frac{13 - x}{4}"
      },
      "name": "input1"
    },
    "hint1": {
      "type": "hint",
      "properties": {
        "content": "Lineariseringen af en funktion [[eql f(x)]]\nomkring punktet [[eql x_0]] er givet ved\n[[eq \nf(x_0) + f'(x_0) \\cdot (x - x_0)\n]]"
      },
      "name": "hint1"
    }
  }
}"""
    for exercise in get_exercises(change_part_of_markup(input_values.splitlines())):
        rendered_exercise = render_exercise(exercise)
        print(rendered_exercise)
        assert_equal(expected_output, rendered_exercise)
        return
    assert False




