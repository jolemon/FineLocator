from argparse import ArgumentParser

regcodes = [
    '185F996AEEC2',
    '7808F4308398',
    'F38075B00218',
    'EBF578C60F6E',
    '00479F7EE8D6'
]

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-a", "--api_path",   dest = "api_path",   required = True)
    args = parser.parse_args()
    api_path = args.api_path

    import sys
    sys.path.append(api_path) # '/Applications/Understand.app/Contents/MacOS/Python'
    import understand as us

    us.license(regcodes[0])

