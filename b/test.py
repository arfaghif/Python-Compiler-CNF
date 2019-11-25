import grammar_converter as gr

gram = gr.read_grammar("a.txt")
print(gram)
print("hore")
gram = gr.convert_grammar(gram)
print(gram)