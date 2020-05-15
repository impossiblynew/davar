import argparse
import parse
import model

def main():
    parser = argparse.ArgumentParser(
        description='Command line tool for the davar experimental intepreted IAL.'
    )
    parser.add_argument('davartext', metavar='DAVARTEXT', type=str)
    parser.add_argument('-l', '--lang', required=False, default=None, help='2 character language code. If not included, davartext will not be translated as it is intepreted.')
    
    args = parser.parse_args()
    print(parse.parse(args.davartext).describe(args.lang))
if __name__ == '__main__':
    main()  