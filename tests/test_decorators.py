from scr.decorators import log


def test_successful_execution(capsys):
    @log()
    def my_function(x, y):
        return x + y

    my_function(1, 2)

    captured = capsys.readouterr()
    assert captured.out == "my_function ok\n\n"


def test_error(capsys):
    @log()
    def my_function(x, y):
        return x / y

    try:
        my_function(1, 0)
    except ZeroDivisionError:
        pass

    captured = capsys.readouterr()
    expected = "my_function error: ZeroDivisionError\n" "Inputs: (1, 0), {}\n" "Traceback:\n"
    assert captured.out.startswith(expected)


def test_logging_to_file(test_file):
    @log(test_file)
    def my_function(x, y):
        return x + y

    my_function(1, 2)

    with open(test_file, "r") as file:
        content = file.read()
        assert content == "my_function ok\n"
