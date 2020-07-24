#!/usr/bin/env python
import parser
import visitor

def main():
    try:
        # p = parser.Parser("msg(AH):description")
        # p = parser.Parser("msg(AH): description")
        # p = parser.Parser("msg:description")
        # p = parser.Parser("message!: description")
        p = parser.Parser("message(SCOPE)!: description")
        # p = parser.Parser("message(SCOPE): description")
        ast = p.parse()
        # printer = visitor.Printer()
        walker = visitor.Walker()

        ast.accept(walker)
    except RuntimeError as error:
        print(error)

if __name__ == "__main__":
    main()
