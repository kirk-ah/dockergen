from test import flask_tests, django_tests, base_image_tests
if __name__ == "__main__":
    # django_tests.run_examples()
    # flask_tests.run_examples() # dummy dummmy stupid port
    base_image_tests.test_all_base_images()