/*
 * py_lexer.l - Simple Python lexer using 
 flex py_lexer.l
gcc lex.yy.c -o py_lexer -lfl
./py_lexer input.py
 */

%{
#include <stdio.h>
extern FILE *yyin;
int line_num = 1;
%}

%option noyywrap

DIGIT    [0-9]
LETTER   [a-zA-Z_]
ID       {LETTER}({LETTER}|{DIGIT})*
INT      {DIGIT}+
FLOAT    {DIGIT}+"."{DIGIT}+
STR_DQ   \"([^\\\"]|\\.)*\"
STR_SQ   \'([^\\\']|\\.)*\'

%%

"if"|"else"|"elif"|"while"|"for"|"def"|"return"|"class"|"import"|"True"|"False"|"None"|"and"|"or"|"not"|"in"|"is"|"pass"|"break"|"continue" { printf("Line %d: KEYWORD        (%s)\n", line_num, yytext); }

"**"|"//"|"=="|"!="|">="|"<="|"+="|"-=" { printf("Line %d: OPERATOR       (%s)\n", line_num, yytext); }
[+\-*/%=<>]                                { printf("Line %d: OPERATOR       (%s)\n", line_num, yytext); }

[()\[\]{},:.]                              { printf("Line %d: DELIMITER      (%s)\n", line_num, yytext); }

{STR_DQ}|{STR_SQ}                          { printf("Line %d: STRING         (%s)\n", line_num, yytext); }
{FLOAT}                                    { printf("Line %d: FLOAT          (%s)\n", line_num, yytext); }
{INT}                                      { printf("Line %d: INTEGER        (%s)\n", line_num, yytext); }

{ID}                                       { printf("Line %d: IDENTIFIER     (%s)\n", line_num, yytext); }

"#"[^\n]*                                  { /* single-line comment */ }
[ \t]+                                     { /* whitespace */ }
\r\n|\n|\r                                 { line_num++; }

.                                          { printf("Line %d: UNKNOWN        (%s)\n", line_num, yytext); }

%%

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *f = fopen(argv[1], "r");
        if (!f) {
            fprintf(stderr, "Cannot open %s\n", argv[1]);
            return 1;
        }
        yyin = f;
    }
    yylex();
    return 0;
}
