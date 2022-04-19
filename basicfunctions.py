#função pra colocar em um while loop perguntando alguma coisa e se deseja continuar
def ask_ok(prompt, follow="Continando "):
    while True:
            ok = input(prompt)
            if ok in ["SIM", "SI", "S", "sim", "si", "s", "ok"]:
                print(follow)
                return True
            elif ok in ["n", "na", "nao", "não", "nã" "N", "NA", "NÃ", "NÃO", "NAO"]:
                print("\nEntão digite novamente ")
                return False
            else:
                print("\nPOR FAVOR DIGITE SIM OU NAO")
           
if __name__ == "__main__":
    while True:
        dataNasc = input("Digite sua data de nascimento com barras (ex. 01/01/1900): ")
        if ask_ok("A data " + '\033[1m' + dataNasc + "\033[0;0m" +" está correta? ", "Continuando com a data: " + '\033[1m' + dataNasc + "\033[0;0m")==True:
            break
