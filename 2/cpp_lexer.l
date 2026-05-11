/*
 * cpp_lexer.l — Simple C++ Lexer using Flex
 *
 * HOW TO BUILD AND RUN:
 * ---------------------
 *   flex cpp_lexer.l
 *   gcc lex.yy.c -o cpp_lexer -lfl
 *   ./cpp_lexer input.cpp
 *
 * WHAT IT HANDLES:
 *   Keywords, Identifiers, Integer & Float literals,
 *   String literals, Operators, Delimiters, Comments, Errors
 */

%{
#include <stdio.h>
int line_num = 1;
%}

%option noyywrap

/* Reusable patterns */
DIGIT    [0-9]
LETTER   [a-zA-Z_]
ID       {LETTER}({LETTER}|{DIGIT})*
INT      {DIGIT}+
FLOAT    {DIGIT}+"."{DIGIT}+
STR      \"([^\\\"]|\\.)*\"

%%

/* ── Keywords ── */
"int"|"float"|"double"|"char"|"void"|"bool"|"if"|"else"|"while"|"for"|"do"|"return"|"class"|"public"|"private"|"protected"|"new"|"delete"|"true"|"false"|"nullptr"|"include"|"using"|"namespace"|"cout"|"cin"|"endl"
    { printf("Line %d: KEYWORD        (%s)\n", line_num, yytext); }

/* ── Operators (multi-char first, then single-char) ── */
"++"|"--"|"=="|"!="|">="|"<="|"&&"|"||"|"+="|"-="|"->"|"::"
    { printf("Line %d: OPERATOR       (%s)\n", line_num, yytext); }
[+\-*/%=<>&|!~^]
    { printf("Line %d: OPERATOR       (%s)\n", line_num, yytext); }

/* ── Delimiters ── */
[()[\]{},;:.]   { printf("Line %d: DELIMITER      (%s)\n", line_num, yytext); }

/* ── Literals ── */
{STR}   { printf("Line %d: STRING         (%s)\n", line_num, yytext); }
{FLOAT} { printf("Line %d: FLOAT          (%s)\n", line_num, yytext); }
{INT}   { printf("Line %d: INTEGER        (%s)\n", line_num, yytext); }

/* ── Identifier (must come after keywords) ── */
{ID}    { printf("Line %d: IDENTIFIER     (%s)\n", line_num, yytext); }

/* ── Ignored ── */
"//".*          { /* single-line comment, skip */ }
"/*"([^*]|\*+[^*/])*"*/"  { /* multi-line comment — count newlines inside it */ 
                              for (char *p = yytext; *p; p++) if (*p == '\n') line_num++; }
[ \t]           { /* whitespace, skip */ }
\n              { line_num++; }

/* ── Anything else is an error ── */
.   { printf("Line %d: UNKNOWN        (%s)\n", line_num, yytext); }

%%

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *f = fopen(argv[1], "r");
        if (!f) { fprintf(stderr, "Cannot open %s\n", argv[1]); return 1; }
        yyin = f;
    }
    yylex();
    return 0;
}