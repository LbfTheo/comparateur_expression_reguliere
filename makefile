CCL = flex # Compilateur flex (anciennement lex)
CCY = bison # Compilateur bison (anciennement yacc)
CC = gcc # Compilateur C
BOPTIONS = -d -y # Permet de générer une sortie dans le Format Yacc standard option du compilateur Yacc
COPTIONS = -O2 -Wall -Wextra # Options du compilateur de C
CYOPTIONS = -Wconsflicts-sr -Wconsflicts-rr -Wcounterexamples
TARGET = generator

all: $(TARGET)

lex.yy.c: regexp.l y.tab.h # Compiler le fichier lex
	@$(CCL) $<

y.tab.c y.tab.h: regexp.y # Compiler le fichier yacc
	@$(CCY) $(BOPTIONS) $<

$(TARGET): lex.yy.c y.tab.c # Compiler les fichiers c de lex et bison
	@$(CC) $(COPTIONS) $^ -o $@

clean:
	@rm -f lex.yy.c y.tab.c y.tab.h script.py