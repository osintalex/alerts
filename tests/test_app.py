from app.alerts import Alerts

# Run this with python -m pytest tests/ from project root
# Instantiate class for testing
alerts_testing = Alerts()


def test_get_listing(requests_mock):
    """
    Requests-mock replaces any requests made in the test with a mocking object. This function mostly just sends a GET
    request so this is very helpful.
    """

    requests_mock.get(
        "https://test.com", content=b"data"
    )  # this makes the response object binary data b'data
    assert b"data" == alerts_testing.get_listing(
        listing=("test_listing", "https://test.com")
    )


def test_check_for_updates(tmp_path):
    """
    tmp_path is a pytest fixture which will provide a temporary directory unique to this test, i.e. this means you
    won't mess up all the files in the application root. Since the function being tested writes files and opens them
    this is helpful!
    """

    actual = alerts_testing.check_for_updates(
        listing=("test_listing", "https://www.testurl.com"), new_listing=b"test"
    )
    expected = ("test_listing", "https://www.testurl.com")

    assert expected == actual


def test_send_email():
    """
    There are libraries to do this if it's going to clients but since it's just for me have just tested it all.
    """

    actual = alerts_testing.send_email(
        listing=("test_listing", "https://www.testurl.com")
    )
    expected = None  # the above method should return an empty dictionary unless there are errors with the sending

    assert actual == expected
