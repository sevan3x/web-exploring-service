import sys, getopt

from web_exploring_service import WebExploringService


def main():
    args_given = _parse_arguments(sys.argv[1:])
    print("Starting Web Exploring Service...")
    wes_client = WebExploringService(args_given["main_url"], args_given["number_of_pages"])

    if args_given["main_url"] and args_given["number_of_pages"]:
        if not wes_client.check_if_server_is_alive():
            print("Server is not reachable.")

        wes_client.take_screenshots()

    elif args_given["screenshot_id"]:
        screenshots_found = wes_client.get_screenshots_by_id(args_given["screenshot_id"])
        print(screenshots_found)


def _parse_arguments(argv):
    arguments_to_return = {
        "main_url": None,
        "number_of_pages": None,
        "screenshot_id": None,
    }

    try:
        opts, args = getopt.getopt(argv, "hu:n:g:", ["mainUrl=", "numberOfPages=", "getScreenshotsById="])
    except getopt.GetoptError:
        print('screenshot_service.py -u <mainUrl> -n <numberOfPages>')
        print('or screenshot_service.py -g <screenshotId>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Use the service as follows:')
            print('1. Take screenshots:')
            print('screenshot_service.py -u <mainUrl> -n <numberOfPages>')
            print('2. Get screenshots by ID:')
            print('or screenshot_service.py -g <screenshotId>')
            sys.exit()
        elif opt in ("-u", "--mainUrl"):
            arguments_to_return["main_url"] = arg
        elif opt in ("-n", "--numberOfPages"):
            arguments_to_return["number_of_pages"] = int(arg)
        elif opt in ("-g", "--getScreenshotsById"):
            arguments_to_return["screenshot_id"] = arg

    if arguments_to_return["main_url"] and arguments_to_return["number_of_pages"]:
        return arguments_to_return
    elif arguments_to_return["screenshot_id"]:
        return arguments_to_return
    elif arguments_to_return["main_url"] and not arguments_to_return["number_of_pages"]:
        print("There is a missing argument. Please use as follows:")
        print('1. Take screenshots:')
        print('screenshot_service.py -u <mainUrl> -n <numberOfPages>')
        print('2. Get screenshots by ID:')
        print('or screenshot_service.py -g <screenshotId>')
    elif not arguments_to_return["main_url"] and arguments_to_return["number_of_pages"]:
        print("There is a missing argument. Please use as follows:")
        print('1. Take screenshots:')
        print('screenshot_service.py -u <mainUrl> -n <numberOfPages>')
        print('2. Get screenshots by ID:')
        print('or screenshot_service.py -g <screenshotId>')
    else:
        print("Error while executing. Please use as follows:")
        print('1. Take screenshots:')
        print('screenshot_service.py -u <mainUrl> -n <numberOfPages>')
        print('2. Get screenshots by ID:')
        print('or screenshot_service.py -g <screenshotId>')

    sys.exit()


if __name__ == "__main__":
    main()
