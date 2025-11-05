const logo = document.getElementById("logo");
const homeBtn = document.getElementById("home-btn");
const menuBtn = document.getElementById("menu-btn");
const jogosBtn = document.getElementById("games-btn");

homeBtn.addEventListener('click', () => {
	window.location.href = "index.html";
});

menuBtn.addEventListener('click', () => {
	window.location.href = "menu.html";
});

jogosBtn.addEventListener('click', () => {
	window.location.href = "games.html";
});

document.addEventListener('DOMContentLoaded', async () => {
	try {
		const [jogosRes, cardapioRes] = await Promise.all([
			fetch('back/.venv/data/jogos.json'),
			fetch('back/.venv/data/cardapio.json')
		]);

		const [jogos, cardapio] = await Promise.all([
			jogosRes.json(),
			cardapioRes.json()
		]);

		console.log('Jogos:', jogos);
		console.log('Cardápio:', cardapio);

		const jogosLista = document.getElementById('jogos-lista');
		if (jogosLista && Array.isArray(jogos)) {
			jogosLista.innerHTML = jogos.map(g => `
				<li>${g.nome || ''} — ${g.estilo || ''} (${g.jogadores || ''})</li>
			`).join('');
		}

		const menuLista = document.getElementById('menu-lista');
		if (menuLista && Array.isArray(cardapio)) {
			menuLista.innerHTML = cardapio.map(i => `
				<li>${i.tipo || ''}: ${i.nome || ''} — ${i.preco != null ? 'R$ ' + i.preco : ''}</li>
			`).join('');
		}
	} catch (err) {
		console.error('Erro ao buscar dados:', err);
	}
});