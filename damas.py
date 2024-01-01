import random
import sys
import pygame

def startboard():
	Matriz = []
	for i in range(0,8):
		Matriz.append([])
		col=0
		for j in range(0,8):
			if i<3 and (j+1)%2==0:
				if i%2==1: 
					col=1
				else:
					col=0
				Matriz[i].insert((j-col),'B')
			elif i>4 and (j+1)%2==0:
				if i%2==1: 
					col=-1
				else:
					col=0
				Matriz[i].insert((j+col),'P')
			else:
				Matriz[i].append('-')
	return Matriz



cor_inicial = 'P'
tabuleiro = startboard()#data
jogo_iniciado = False
#Parte gráfica (pygame)
WIDTH, HEIGHT = 400, 400
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Damas")

pygame.init()


def menu_principal():
	screen.fill(BROWN)
	title_font = pygame.font.Font(None, 48)
	title_text = title_font.render("Checkers Game", True, WHITE)
	title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
	screen.blit(title_text, title_rect)

	subtitle_font = pygame.font.Font(None, 24)
	subtitle_text1 = subtitle_font.render("Aperte B para começar com as brancas", True, WHITE)
	subtitle_rect1 = subtitle_text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
	screen.blit(subtitle_text1, subtitle_rect1)

	subtitle_text2 = subtitle_font.render("Aperte P para começar com as pretas", True, WHITE)
	subtitle_rect2 = subtitle_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2))
	screen.blit(subtitle_text2, subtitle_rect2)

	subtitle_text3 = subtitle_font.render("Pressione ENTER para o computador jogar automaticamente", True, WHITE)
	subtitle_rect3 = subtitle_text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
	screen.blit(subtitle_text3, subtitle_rect3)

	subtitle_text4 = subtitle_font.render("O botão R reinicia o programa", True, WHITE)
	subtitle_rect4 = subtitle_text4.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
	screen.blit(subtitle_text4, subtitle_rect4)

	pygame.display.flip()

	tela_menu = True
	while tela_menu:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					cor_inicial = 'P'
					tela_menu = False
				elif event.key == pygame.K_b:
					print("Iniciando com as brancas")
					cor_inicial = 'B'
					tela_menu = False
				elif event.key == pygame.K_p:
					print("Iniciando com as pretas")
					cor_inicial = 'P'
					tela_menu = False
	return True, cor_inicial

def desenha_tabuleiro():
	BROWN = (139, 69, 19)
	GRAY_WHITE = (211, 211, 211)
	DARK_GRAY = (55, 55, 55)
	YELLOW_WHITE = (255, 255, 0)
	WHITE = (255, 255, 255)
	CELL_SIZE = WIDTH // 8

	for row in range(8):
		for col in range(8):
			color = GRAY_WHITE if (row + col) % 2 == 0 else BROWN
			pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

			piece = tabuleiro[row][col]
			if piece == 'B':  # White piece
				pygame.draw.circle(screen, GRAY_WHITE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
			elif piece == 'P':  # Black piece
				pygame.draw.circle(screen, DARK_GRAY, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
			if piece == 'BD':
				pygame.draw.circle(screen, GRAY_WHITE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
				pygame.draw.circle(screen, YELLOW_WHITE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2, width=2)
			elif piece == 'PD':
				pygame.draw.circle(screen, DARK_GRAY, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
				pygame.draw.circle(screen, YELLOW_WHITE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2, width=2)

def inside(linha, coluna):
	if linha >= 0 and linha < 8 and coluna >= 0 and coluna < 8:
		return True
	else:
		return False

def peca_captura(linha, coluna, direcao):
	if direcao == 0: #Se estiver capturando a peça na diagonal esquerda de cima
		if inside(linha-1, coluna-1):
			if tabuleiro[linha-1][coluna-1] == '-':
				return True
			else:
				return False
	elif direcao == 1: #Se estiver capturando a peça na diagonal esquerda de baixo
		if inside(linha+1, coluna-1):
			if tabuleiro[linha+1][coluna-1] == '-':
				return True
			else:
				return False
	elif direcao == 2: #Se estiver capturando a peça na diagonal direita de cima
		if inside(linha-1, coluna+1):
			if tabuleiro[linha-1][coluna+1] == '-':
				return True
			else:
				return False
	elif direcao == 3: #Se estiver capturando a peça na diagonal direita de baixo
		if inside(linha+1, coluna+1):
			if tabuleiro[linha+1][coluna+1] == '-':
				return True
			else:
				return False
	return False

def checa_brancas(linha, coluna):
	movimentos_encontrados = []

	if inside(linha+1,coluna-1): #Verifica se está nas margens do tabuleiro caso contrário geraria erro
		if tabuleiro[linha+1][coluna-1] == '-': # Verifica se o espaço da esquerda está vazio
			if linha == 6: # Se estava perto de virar dama:
				movimentos_encontrados.append([linha, coluna, linha+1, coluna-1, 1, 0])
			else:
				movimentos_encontrados.append([linha, coluna, linha+1, coluna-1, 0, 0])
		elif tabuleiro[linha+1][coluna-1] == 'P' or tabuleiro[linha+1][coluna-1] == 'PD': #Verifica se é um inimigo
			if peca_captura(linha+1, coluna-1, 1): #Verifica se é possível capturar o inimigo
				movimentos_encontrados.append([linha, coluna, linha+2, coluna-2, 2, 1, linha+1, coluna-1])
	if inside(linha+1, coluna +1): # Verifica se o espaço da direita está vazio
		if tabuleiro[linha+1][coluna+1] == '-':
			movimentos_encontrados.append([linha, coluna, linha+1, coluna+1, 0, 3])
		elif tabuleiro[linha+1][coluna+1] == 'P' or tabuleiro[linha+1][coluna+1] == 'PD': #Verifica se é um inimigo
			if peca_captura(linha+1, coluna+1, 3):
				movimentos_encontrados.append([linha, coluna, linha+2, coluna+2, 2, 3, linha+1, coluna+1])
	return movimentos_encontrados

def checa_pretas(linha, coluna):
	movimentos_encontrados = []
	if inside(linha-1,coluna-1): #Verifica se está nas margens do tabuleiro caso contrário geraria erro
		if tabuleiro[linha-1][coluna-1] == '-': # Verifica se o espaço está vazio
			if linha == 1: # Se está perto de virar dama
				movimentos_encontrados.append([linha, coluna, linha-1, coluna-1, 1, 1])
			else:
				movimentos_encontrados.append([linha, coluna, linha-1, coluna-1, 0, 0])
		elif tabuleiro[linha-1][coluna-1] == 'B' or tabuleiro[linha-1][coluna-1] == 'BD': #Verifica se é um inimigo
			if peca_captura(linha-1, coluna-1, 0): #Verifica se é possível capturar o inimigo
				movimentos_encontrados.append([linha, coluna, linha-2, coluna-2, 2, 0, linha-1, coluna-1])
	if inside(linha-1, coluna +1):
		if tabuleiro[linha-1][coluna+1] == '-':
			if linha == 1: # Se está perto de virar dama
				movimentos_encontrados.append([linha, coluna, linha-1, coluna+1, 1, 3])
			else:
				movimentos_encontrados.append([linha, coluna, linha-1, coluna+1, 0, 2])
		elif tabuleiro[linha-1][coluna+1] == 'B' or tabuleiro[linha-1][coluna+1] == 'BD': #Verifica se é um inimigo
			if peca_captura(linha-1, coluna+1, 2):
				movimentos_encontrados.append([linha, coluna, linha-2, coluna+2, 2, 2, linha-1, coluna+1])
	return movimentos_encontrados


def dama_captura(linha, coluna, aliados):
	if aliados == 'B':
		damaAliada = 'BD'
		inimigos = 'P'
		damaInimiga = 'PD'
	else:
		damaAliada = 'PD'
		inimigos = 'B'
		damaInimiga = 'BD'

	linha_cima_esquerda = linha
	coluna_cima_esquerda = coluna
	while inside(linha_cima_esquerda-1, coluna_cima_esquerda-1): # Percorre pela parte de cima esquerda da dama e adiciona os movimentos
		linha_cima_esquerda -= 1
		coluna_cima_esquerda -= 1
		# Se uma peça aliada impedir o movimento, a dama nao pode mais se mover na direção
		if tabuleiro[linha_cima_esquerda][coluna_cima_esquerda] == aliados or tabuleiro[linha_cima_esquerda][coluna_cima_esquerda] == damaAliada: 
			break

		elif tabuleiro[linha_cima_esquerda][coluna_cima_esquerda] == inimigos or tabuleiro[linha_cima_esquerda][coluna_cima_esquerda] == damaInimiga:
			if peca_captura(linha_cima_esquerda, coluna_cima_esquerda, 0): # Verifica se é possível capturar o inimigo
				return True


	linha_baixo_esquerda = linha
	coluna_baixo_esquerda = coluna
	while inside(linha_baixo_esquerda+1, coluna_baixo_esquerda-1):
		linha_baixo_esquerda += 1
		coluna_baixo_esquerda -= 1

		# Se uma peça aliada impedir o movimento, a dama nao pode mais se mover na direção
		if tabuleiro[linha_baixo_esquerda][coluna_baixo_esquerda] == aliados or tabuleiro[linha_baixo_esquerda][coluna_baixo_esquerda] == damaAliada: 
			break
		#Se a dama encontra um inimigo, verifica se ela pode capturá-lo
		elif tabuleiro[linha_baixo_esquerda][coluna_baixo_esquerda] == inimigos or tabuleiro[linha_baixo_esquerda][coluna_baixo_esquerda] == damaInimiga: 
				return True
	
	linha_cima_direita = linha
	coluna_cima_direita = coluna
	while inside(linha_cima_direita-1, coluna_cima_direita+1):
		linha_cima_direita -= 1
		coluna_cima_direita += 1

		# Se uma peça aliada impedir o movimento, a dama nao pode mais se mover na direção
		if tabuleiro[linha_cima_direita][coluna_cima_direita] == aliados or tabuleiro[linha_cima_direita][coluna_cima_direita] == damaAliada: 
			break
		#Se a dama encontra um inimigo, verifica se ela pode capturá-lo
		elif tabuleiro[linha_cima_direita][coluna_cima_direita] == inimigos or tabuleiro[linha_cima_direita][coluna_cima_direita] == damaInimiga: 
			if peca_captura(linha_cima_direita, coluna_cima_direita, 2):
				return True
	
	linha_baixo_direita = linha
	coluna_baixo_direita = coluna
	while inside(linha_baixo_direita+1, coluna_baixo_direita+1):
		linha_baixo_direita += 1
		coluna_baixo_direita += 1

		# Se uma peça aliada impedir o movimento, a dama nao pode mais se mover na direção
		if tabuleiro[linha_baixo_direita][coluna_baixo_direita] == aliados or tabuleiro[linha_baixo_direita][coluna_baixo_direita] == damaAliada: 
			break
		#Se a dama encontra um inimigo, verifica se ela pode capturá-lo
		elif tabuleiro[linha_baixo_direita][coluna_baixo_direita] == inimigos or tabuleiro[linha_baixo_direita][coluna_baixo_direita] == damaInimiga: 
			if peca_captura(linha_baixo_direita, coluna_baixo_direita, 3):
				return True

	return False

def checa_dama(linha, coluna, aliados):
	if aliados == 'B':
		damaAliada = 'BD'
		inimigos = 'P'
		damaInimiga = 'PD'
	else:
		damaAliada = 'PD'
		inimigos = 'B'
		damaInimiga = 'BD'

	movimentos_encontrados = []

	linha_cima_esquerda = linha
	coluna_cima_esquerda = coluna
	while inside(linha_cima_esquerda-1, coluna_cima_esquerda-1): # Percorre pela parte de cima esquerda da dama e adiciona os movimentos
		linha_cima_esquerda -= 1
		coluna_cima_esquerda -= 1
		if tabuleiro[linha_cima_esquerda][coluna_cima_esquerda] == '-':
			movimentos_encontrados.append([linha, coluna, linha_cima_esquerda, coluna_cima_esquerda, 0, 0])

		# Se uma peça aliada impedir o movimento, a dama nao pode mais se mover na direção
		elif tabuleiro[linha_cima_esquerda][coluna_cima_esquerda] == aliados or tabuleiro[linha_cima_esquerda][coluna_cima_esquerda] == damaAliada: 
			break

		elif tabuleiro[linha_cima_esquerda][coluna_cima_esquerda] == inimigos or tabuleiro[linha_cima_esquerda][coluna_cima_esquerda] == damaInimiga:
			if peca_captura(linha_cima_esquerda, coluna_cima_esquerda, 0): # Verifica se é possível capturar o inimigo
				movimentos_encontrados.append([linha, coluna, linha_cima_esquerda-1, coluna_cima_esquerda-1, 2, 0, linha_cima_esquerda, coluna_cima_esquerda])
				break
		else:
			break


	linha_baixo_esquerda = linha
	coluna_baixo_esquerda = coluna
	while inside(linha_baixo_esquerda+1, coluna_baixo_esquerda-1):
		linha_baixo_esquerda += 1
		coluna_baixo_esquerda -= 1
		if tabuleiro[linha_baixo_esquerda][coluna_baixo_esquerda] == '-':
			movimentos_encontrados.append([linha, coluna, linha_baixo_esquerda, coluna_baixo_esquerda, 0, 1])

		# Se uma peça aliada impedir o movimento, a dama nao pode mais se mover na direção
		elif tabuleiro[linha_baixo_esquerda][coluna_baixo_esquerda] == aliados or tabuleiro[linha_baixo_esquerda][coluna_baixo_esquerda] == damaAliada: 
			break
		#Se a dama encontra um inimigo, verifica se ela pode capturá-lo
		elif tabuleiro[linha_baixo_esquerda][coluna_baixo_esquerda] == inimigos or tabuleiro[linha_baixo_esquerda][coluna_baixo_esquerda] == damaInimiga: 
			if peca_captura(linha_baixo_esquerda, coluna_baixo_esquerda, 1):
				movimentos_encontrados.append([linha, coluna, linha_baixo_esquerda+1, coluna_baixo_esquerda-1, 2, 1, linha_baixo_esquerda, coluna_baixo_esquerda])
				break
		else:
			break
	
	linha_cima_direita = linha
	coluna_cima_direita = coluna

	while inside(linha_cima_direita-1, coluna_cima_direita+1):
		linha_cima_direita -= 1
		coluna_cima_direita += 1
		if tabuleiro[linha_cima_direita][coluna_cima_direita] == '-':
			movimentos_encontrados.append([linha, coluna, linha_cima_direita, coluna_cima_direita, 0, 2])

		# Se uma peça aliada impedir o movimento, a dama nao pode mais se mover na direção
		elif tabuleiro[linha_cima_direita][coluna_cima_direita] == aliados or tabuleiro[linha_cima_direita][coluna_cima_direita] == damaAliada: 
			break
		#Se a dama encontra um inimigo, verifica se ela pode capturá-lo
		elif tabuleiro[linha_cima_direita][coluna_cima_direita] == inimigos or tabuleiro[linha_cima_direita][coluna_cima_direita] == damaInimiga: 
			if peca_captura(linha_cima_direita, coluna_cima_direita, 2):
				movimentos_encontrados.append([linha, coluna, linha_cima_direita-1, coluna_cima_direita+1, 2, 3, linha_cima_direita, coluna_cima_direita])
				break
		else:
			break
	
	linha_baixo_direita = linha
	coluna_baixo_direita = coluna

	while inside(linha_baixo_direita+1, coluna_baixo_direita+1):
		linha_baixo_direita += 1
		coluna_baixo_direita += 1
		if tabuleiro[linha_baixo_direita][coluna_baixo_direita] == '-':
			movimentos_encontrados.append([linha, coluna, linha_baixo_direita, coluna_baixo_direita, 0, 3])

		# Se uma peça aliada impedir o movimento, a dama nao pode mais se mover na direção
		elif tabuleiro[linha_baixo_direita][coluna_baixo_direita] == aliados or tabuleiro[linha_baixo_direita][coluna_baixo_direita] == damaAliada: 
			break
		#Se a dama encontra um inimigo, verifica se ela pode capturá-lo
		elif tabuleiro[linha_baixo_direita][coluna_baixo_direita] == inimigos or tabuleiro[linha_baixo_direita][coluna_baixo_direita] == damaInimiga: 
			if peca_captura(linha_baixo_direita, coluna_baixo_direita, 3):
				movimentos_encontrados.append([linha, coluna, linha_baixo_direita+1, coluna_baixo_direita+1, 2, 4, linha_baixo_direita, coluna_baixo_direita])
				break
		else:
			break

	return movimentos_encontrados


def checa_movimentos_possiveis(linha, coluna, aliados, dama=False):
	if dama:
		movimentos_encontrados = checa_dama(linha, coluna, aliados)
	else: 
		if aliados == 'B' or aliados == 'BD':
			movimentos_encontrados = (checa_brancas(linha, coluna))
		else:
			movimentos_encontrados = (checa_pretas(linha, coluna))

	
	if movimentos_encontrados:
		for i, movimento in enumerate(movimentos_encontrados): #Prioriza capturas múltiplas
			if movimento[4] == 2: # Se for uma captura
				if dama:
					if dama_captura(movimento[2], movimento[3], aliados):
						movimentos_encontrados[i][4] = 3
						return movimento
					else:
						return movimento
				if tem_captura_multipla(movimento[2], movimento[3], aliados):
					movimentos_encontrados[i][4] = 3
					return movimento
				else:
					return movimento
				
		aleatorio = random.randint(0, len(movimentos_encontrados) - 1)
		return (movimentos_encontrados[aleatorio])
	else: # Se nao houver movimentos possíveis para a peça
		return False

def moveAliado(aliados):
	if aliados == 'B':
		damaAliada = 'BD'
	else:
		damaAliada = 'PD'
	movimentos = []

	for i in range(8):
		for j in range(8):
			if tabuleiro[i][j] == aliados:
				movimento_encontrado = checa_movimentos_possiveis(i, j, aliados)
			elif tabuleiro[i][j] == damaAliada:
				movimento_encontrado = checa_movimentos_possiveis(i, j, aliados, True)
			else:
				continue
			if movimento_encontrado:
				movimentos.append(movimento_encontrado)

	for movimento in movimentos: #Prioriza captura múltipla
		if movimento[4] == 3:
			return movimento
	for movimento in movimentos: #Priozira captura simples
		if movimento[4] == 2:
			return movimento
	
	for movimento in movimentos: # Prioriza virar dama
		if movimento[4] == 1:
			return movimento
		
	#Se for um movimento normal , escolhe um aleatório
	if movimentos:
		if len(movimentos) > 1:
			aleatorio = random.randint(0, len(movimentos) - 1)
			return (movimentos[aleatorio])	
		else:
			return (movimentos[0])
	return False
		

def transforma_dama():
	for i in range(8): # Percorre pelas colunas nas extremidades e verifica se alguma peça se tornou dama
		if tabuleiro[0][i] == 'P':
			tabuleiro[0][i] = 'PD'
		elif tabuleiro[7][i] == 'B':
			tabuleiro[7][i] = 'BD'

def captura(linha, coluna, linha_inimigo, coluna_inimigo, linha_destino, coluna_destino):
		if tabuleiro[linha][coluna] == 'PD' or tabuleiro[linha][coluna] == 'BD': # Captura da dama
			tabuleiro[linha_destino][coluna_destino] = tabuleiro[linha][coluna] # Chegando na posição final depois de capturar
			tabuleiro[linha][coluna] = '-' # A peça capturando se moveu
			tabuleiro[linha_inimigo][coluna_inimigo] = '-' #Capturando a peça inimiga
			desenha_tabuleiro()
			pygame.display.flip()

			sequencia_captura = tem_captura_multipla(linha_destino, coluna_destino, tabuleiro[linha_destino][coluna_destino], True)
			if sequencia_captura:
				tecla_apertada = False
				while not tecla_apertada:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:	
							captura(sequencia_captura[0], sequencia_captura[1], sequencia_captura[6], sequencia_captura[7], sequencia_captura[2], sequencia_captura[3])
							tecla_apertada = True

		else: #Captura da peça comum
			tabuleiro[linha_destino][coluna_destino] = tabuleiro[linha][coluna] # Chegando na posição final depois de capturar
			tabuleiro[linha][coluna] = '-' # A peça capturando se moveu
			tabuleiro[linha_inimigo][coluna_inimigo] = '-' #Capturando a peça inimiga
			
			desenha_tabuleiro()
			pygame.display.flip()

			sequencia_captura = tem_captura_multipla(linha_destino, coluna_destino, tabuleiro[linha_destino][coluna_destino])
			if sequencia_captura:
				tecla_apertada = False
				while not tecla_apertada:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:	
							captura(sequencia_captura[0], sequencia_captura[1], sequencia_captura[6], sequencia_captura[7], sequencia_captura[2], sequencia_captura[3])
							tecla_apertada = True
			

def tem_captura_multipla(linha_destino, coluna_destino, aliados, dama=False):
	if dama:
		movimentos_possiveis_apos_captura = checa_movimentos_possiveis(linha_destino, coluna_destino, aliados, True)
	else:
		movimentos_possiveis_apos_captura = checa_movimentos_possiveis(linha_destino, coluna_destino, aliados)
		
	if movimentos_possiveis_apos_captura:
		if movimentos_possiveis_apos_captura[4] == 2 or movimentos_possiveis_apos_captura[4] == 3:
			return movimentos_possiveis_apos_captura
	return False


def move(aliados, inimigos):

	movimento_encontrado = moveAliado(aliados)
	if movimento_encontrado:
		if movimento_encontrado[4] == 3 or movimento_encontrado[4] == 2: # Se o movimento que foi encontrado for do tipo captura múltipla ou captura simples
			captura(movimento_encontrado[0], movimento_encontrado[1], movimento_encontrado[6], movimento_encontrado[7], movimento_encontrado[2], movimento_encontrado[3])
		else:
			tabuleiro[movimento_encontrado[2]][movimento_encontrado[3]] = tabuleiro[movimento_encontrado[0]][movimento_encontrado[1]]
			tabuleiro[movimento_encontrado[0]][movimento_encontrado[1]] = '-'
			
		transforma_dama() # Verifica se alguma peça se tornou dama após o movimento
		return True
	
	print("Parece que não foi possível encontrar nenhum movimento possível para as peças {}.".format(aliados))
	print("Fim de Jogo.")
	return False

def troca_vez(cor):
	if cor == 'B':
		return 'P'
	else:
		return 'B'

while True:
	if not jogo_iniciado:
		jogo_iniciado, cor_inicial = menu_principal()
	if cor_inicial == 'B':
		aliados = 'B'
		damaAliada = 'BD'
		inimigos = 'P'
		damaInimiga = 'PD'
	else:
		aliados = 'P'
		damaAliada = 'PD'
		inimigos = 'B'
		damaInimiga = 'BD'
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				print("É a vez das peças {}.".format(inimigos))
				encontrou_movimento = move(aliados, inimigos)
				if not encontrou_movimento:
					break
				cor_inicial = troca_vez(cor_inicial)
				

			elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				tabuleiro = startboard()
				jogo_iniciado = False
				round = 1
				continue
			
	screen.fill((255, 255, 255))
	desenha_tabuleiro()

	pygame.display.flip()
	clock.tick(60)