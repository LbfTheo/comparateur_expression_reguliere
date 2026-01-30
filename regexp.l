%{
#include "y.tab.h"
int yywrap(void){ return 1; }
%}

%%
[a-c] { yylval.car = yytext[0]; return CAR; }
"E"   { yylval.car = yytext[0]; return EPSILON;}
"+"   { return UNION;}
"."   {return CONCAT;}
"*"   {return ETOILE;}
"("   {return PAR_O;}                         
")"   {return PAR_F;} 
[ \t] { ; }
\n    {return FIN_LIGNE;}
.     {printf("Erreur : caractère inconnu\n");}
%%

