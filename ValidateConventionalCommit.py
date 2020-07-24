#!/usr/bin/env python
import parser
import visitor

def main():
    try:
        # p = parser.Parser("msg(AH):description")
        # p = parser.Parser("msg(AH): description")
        # p = parser.Parser("msg:description")
        # p = parser.Parser("message!: description")
        # p = parser.Parser("message(SCOPE)!: description this. ...\nTHIS IS THE BODY\nTHIS IS THE FOOTER")
        p = parser.Parser("message(SCOPE)!: description this. ...")
        # p = parser.Parser("message(SCOPE)!: description this. ...")
        # p = parser.Parser("message: description.")
        ast = p.parse()
        # printer = visitor.Printer()
        pretty_printer = visitor.PrettyPrinter()
        # walker = visitor.Walker()

        ast.accept(pretty_printer)
    except RuntimeError as error:
        print(error)


if __name__ == "__main__":
    main()
