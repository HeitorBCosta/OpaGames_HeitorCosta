import asyncio
import websockets
import redis

# Conexão com o servidor Redis
#Essa linha de código em Python está criando um objeto cliente para interagir com um banco de dados Redis.

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# Lista para armazenar conexões de jogadores criando um conjunto de players
players = set()

async def broadcast(message, sender):
    # Envia a mensagem para todos os jogadores, exceto o remetente
    for player in players:
        if player != sender:
            await player.send(message)

async def update_game_state(state):
    # Atualiza o estado do jogo no Redis
    redis_client.set('game_state', state)

async def handler(websocket, path):
    # Adiciona o novo jogador à lista
    players.add(websocket)
    print(f"Novo jogador conectado. Total de jogadores: {len(players)}")

    try:
        # Mantém a conexão aberta enquanto o servidor estiver em execução
        async for message in websocket:
            # Aqui as mensagens recebidas dos jogadores são processadas
            # e enviar as atualizações necessárias para todos os jogadores
            print(f"Recebido: {message}")

            # Exemplo: Envia a mensagem recebida para todos os jogadores
            await broadcast(message, websocket)

            # Exemplo: Atualiza o estado do jogo no Redis
            await update_game_state("Novo estado do jogo aqui")

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Remove o jogador quando a conexão é fechada
        players.remove(websocket)
        print(f"Jogador desconectado. Total de jogadores: {len(players)}")

if __name__ == "__main__":
    # Configuração do servidor WebSocket na porta 8765
    start_server = websockets.serve(handler, "localhost", 8765)

    # Inicia o loop de eventos
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()