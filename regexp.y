%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex();
void yyerror(const char *s) { fprintf(stderr, "Erreur : %s\n", s); }

int compteur = 0;

//initialiser le pointeur vers le fichier de script
FILE *py_script;
%}

%code requires {
    typedef struct {
        char *code;
        int id;
    } variable;
}

%union {
    char car;
    variable chaine;
}

%token <car> CAR EPSILON
%token UNION CONCAT ETOILE PAR_O PAR_F FIN_LIGNE

%type <chaine> expression terme facteur primaire

%start axiome

%%

axiome: 
    expression FIN_LIGNE expression {
        /* 1. Imports Python */
        fprintf(py_script, "from automate import *\n\n");

        /* 2. Code de la première expression */
        fprintf(py_script, "# Expression 1 (a%d)\n", $1.id);
        fprintf(py_script, "%s", $1.code);

        /* 3. Code de la deuxième expression */
        fprintf(py_script, "# Expression 2 (a%d)\n", $3.id);
        fprintf(py_script, "%s", $3.code);

        /* 4. Test d'égalité */
        fprintf(py_script, "\n# Comparaison\n");
        fprintf(py_script, "res1 = tout_faire(a%d)\n", $1.id);
        fprintf(py_script, "res2 = tout_faire(a%d)\n", $3.id);
        
        fprintf(py_script, "if egal(res1, res2):\n");
        fprintf(py_script, "\tprint(\"EGAL\")\n");
        fprintf(py_script, "else:\n");
        fprintf(py_script, "\tprint(\"NON EGAL\")\n");
    }
;

/* --- NIVEAU 1 : UNION (Priorité la plus faible) --- */
expression:
      expression UNION terme { compteur++;
			       $$.id = compteur;
			       char ligne[100];
			       sprintf(ligne, "a%d = union(a%d, a%d)\n", $$.id, $1.id, $3.id);
			       $$.code = malloc(strlen($1.code) + strlen($3.code) + strlen(ligne ) + 20);
			       sprintf($$.code, "%s%s%s",$1.code, $3.code, ligne);}

    | terme { 
        /* Si pas d'union, on remonte simplement le terme */
        $$ = $1;}
;

/* --- NIVEAU 2 : CONCATÉNATION (Priorité moyenne) --- */
terme:
     terme facteur {compteur++;
		    $$.id = compteur;
		    char ligne[100];
		    sprintf(ligne, "a%d = concatenation(a%d, a%d)\n", $$.id, $1.id, $2.id);
		    $$.code = malloc(strlen($1.code) + strlen($2.code) + strlen(ligne ) + 20);
		    sprintf($$.code, "%s%s%s",$1.code, $2.code, ligne);}

    | terme CONCAT facteur {compteur++;
			    $$.id = compteur;
			    char ligne[100];
			    sprintf(ligne, "a%d = concatenation(a%d, a%d)\n", $$.id, $1.id, $3.id);
			    $$.code = malloc(strlen($1.code) + strlen($3.code) + strlen(ligne ) + 20);
			    sprintf($$.code, "%s%s%s",$1.code, $3.code, ligne);}

    | facteur { 
        $$ = $1;}
;

/* --- NIVEAU 3 : ÉTOILE (Priorité forte) --- */
facteur:
     facteur ETOILE {compteur++;
		     $$.id = compteur;
		     char ligne[100];
		     sprintf(ligne, "a%d = etoile(a%d)\n", $$.id, $1.id);
		     $$.code = malloc(strlen($1.code) + strlen(ligne ) + 20);
		     sprintf($$.code, "%s%s",$1.code, ligne);}

    | primaire { 
        $$ = $1;}
;

/* --- NIVEAU 4 : FEUILLES (Les atomes) --- */
primaire:
     PAR_O expression PAR_F {$$.id = $2.id;
       			     $$.code = $2.code;}
    
    | CAR {compteur++;
           $$.id = compteur;
    	   $$.code = malloc(100);
    	   sprintf($$.code, "a%d = automate(\"%c\")\n", $$.id, $1);}

    | EPSILON {compteur++;
   	       $$.id = compteur;
    	       $$.code = malloc(100);
    	       sprintf($$.code, "a%d = automate(\"%c\")\n", $$.id, $1);}
;

%%

int main(void){
    // Création du script
    py_script = fopen("main.py", "w");
    if (py_script == NULL){
        fprintf(stderr, "Impossible de créer le fichier script.py");
        return 1;
    }
    yyparse();
    fclose(py_script);
    return 0;
}