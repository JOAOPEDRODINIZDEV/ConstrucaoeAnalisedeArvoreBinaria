class No:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, chave):
        if not self.raiz:
            self.raiz = No(chave)
        else:
            self._inserir_recursivamente(self.raiz, chave)

    def _inserir_recursivamente(self, no_atual, chave):
        if chave < no_atual.chave:
            if no_atual.esquerda is None:
                no_atual.esquerda = No(chave)
            else:
                self._inserir_recursivamente(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            if no_atual.direita is None:
                no_atual.direita = No(chave)
            else:
                self._inserir_recursivamente(no_atual.direita, chave)

    def buscar(self, chave):
        return self._buscar_recursivamente(self.raiz, chave)

    def _buscar_recursivamente(self, no_atual, chave):
        if no_atual is None:
            return False
        if no_atual.chave == chave:
            return True
        if chave < no_atual.chave:
            return self._buscar_recursivamente(no_atual.esquerda, chave)
        return self._buscar_recursivamente(no_atual.direita, chave)

    def obter_altura(self):
        return self._obter_altura_recursivamente(self.raiz)

    def _obter_altura_recursivamente(self, no_atual):
        if no_atual is None:
            return 0
        altura_esquerda = self._obter_altura_recursivamente(no_atual.esquerda)
        altura_direita = self._obter_altura_recursivamente(no_atual.direita)
        return max(altura_esquerda, altura_direita) + 1

    def contar_nos_internos(self):
        return self._contar_nos_internos_recursivamente(self.raiz)

    def _contar_nos_internos_recursivamente(self, no_atual):
        if no_atual is None:
            return 0
        if no_atual.esquerda or no_atual.direita:
            return 1 + self._contar_nos_internos_recursivamente(no_atual.esquerda) + self._contar_nos_internos_recursivamente(no_atual.direita)
        return 0

    def contar_folhas(self):
        return self._contar_folhas_recursivamente(self.raiz)

    def _contar_folhas_recursivamente(self, no_atual):
        if no_atual is None:
            return 0
        if no_atual.esquerda is None and no_atual.direita is None:
            return 1
        return self._contar_folhas_recursivamente(no_atual.esquerda) + self._contar_folhas_recursivamente(no_atual.direita)

def main():
    arvore_binaria = ArvoreBinaria()
    numeros = [63, 50, 65, 20, 40, 60, 80]
    for num in numeros:
        arvore_binaria.inserir(num)

    print("Raiz da árvore:", arvore_binaria.raiz.chave)
    print("Altura da árvore:", arvore_binaria.obter_altura())
    print("Número de nós internos:", arvore_binaria.contar_nos_internos())
    print("Número de folhas:", arvore_binaria.contar_folhas())

    numero_busca = 50
    if arvore_binaria.buscar(numero_busca):
        print(f"{numero_busca} está presente na árvore.")
    else:
        print(f"{numero_busca} não está presente na árvore.")

if __name__ == "__main__":
    main()
