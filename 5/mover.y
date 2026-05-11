/*
 * mover.y  —  Parser + Syntax-Directed Translation for the grid movement problem
 *
 * The grammar:
 *   S --> S D       (a sequence is built left to right)
 *   S --> START     (every valid sequence starts with the keyword START)
 *   D --> n | s | e | w
 *
 * Syntax-Directed Translation:
 *   Each direction token D carries a semantic action that updates
 *   the global (x, y) position. This is the "translation" part —
 *   the grammar rules directly drive coordinate updates as the
 *   input is parsed.
 *
 * Starting position is always (0, 0).
 * North/South change y. East/West change x.
 */

%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(char *s);
int  yylex();

/* Global coordinates — start at origin */
int x = 0;
int y = 0;
%}

/* Token names shared with the lexer */
%token START N S_DIR E_DIR W_DIR

%%

/*
 * Top-level rule:
 * A valid program is one sequence S followed by a newline.
 * When we reach the newline we print the final position.
 */
Program:
    S '\n'   { printf("Final position is ( %d , %d )\n", x, y); exit(0); }
    ;

/*
 * S rule:
 *   S D   — extend the current sequence with one more direction
 *   START — the sequence begins here; reset coordinates to (0,0)
 */
S:
    S D          /* nothing extra needed; D's action already updated x,y */
  | START        { x = 0; y = 0; }   /* keyword START resets to origin */
  ;

/*
 * D rule — each direction updates the global position.
 * This is where Syntax-Directed Translation happens:
 * the grammar rule for each token directly triggers a coordinate update.
 */
D:
    N       { y++; }    /* north  => move up    */
  | S_DIR   { y--; }    /* south  => move down  */
  | E_DIR   { x++; }    /* east   => move right */
  | W_DIR   { x--; }    /* west   => move left  */
  ;

%%

/*
 * yyerror is called automatically by yacc when the input
 * doesn't match the grammar (e.g. an unknown letter like 'b').
 */
void yyerror(char *s) {
    printf("Invalid string\n");
    exit(1);
}

int main() {
    yyparse();   /* Start parsing; calls yylex() internally */
    return 0;
}