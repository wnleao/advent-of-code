

def readlines():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        required=True,
                        default=None,
                        help='puzzle input filepath (e.g.: "input.txt" or "example.txt")')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        content = f.read().splitlines()

    return content
