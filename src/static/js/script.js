document.addEventListener('DOMContentLoaded', async () => {
    await loadParticipants();
    
    const savedSection = sessionStorage.getItem('activeSection') || 'leaderboard';
    showSection(savedSection);

    const savedUser = sessionStorage.getItem('selectedUser');
    if (savedUser) {
        const select = document.getElementById('userSelect');
        select.value = savedUser;
        loadUserResults();
    }
});

function showSection(sectionId) {
    sessionStorage.setItem('activeSection', sectionId);
    document.getElementById('leaderboard').style.display = sectionId === 'leaderboard' ? 'block' : 'none';
    document.getElementById('individual').style.display = sectionId === 'individual' ? 'block' : 'none';
    
    if (sectionId === 'leaderboard') loadLeaderboard();
}

async function loadLeaderboard() {
    const response = await fetch('/api/leaderboard');
    const data = await response.json();
    const tbody = document.querySelector('#leaderboardTable tbody');
    tbody.innerHTML = '';

    data.forEach((row, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${row.Participante}</td>
            <td><strong>${row.Puntos}</strong></td>
        `;
        tbody.appendChild(tr);
    });
}

async function loadParticipants() {
    const response = await fetch('/api/participants');
    const participants = await response.json();
    const select = document.getElementById('userSelect');
    
    participants.forEach(name => {
        const option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        select.appendChild(option);
    });
}

async function loadUserResults() {
    const name = document.getElementById('userSelect').value;
    if (!name) {
        sessionStorage.removeItem('selectedUser');
        return;
    }

    sessionStorage.setItem('selectedUser', name);

    const response = await fetch(`/api/user_results/${encodeURIComponent(name)}`);
    const data = await response.json();
    
    const tbody = document.querySelector('#resultsTable tbody');
    const summary = document.getElementById('userSummary');
    tbody.innerHTML = '';

    let totalPoints = 0;
    data.forEach(row => {
        totalPoints += (row.Puntos || 0);
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.Tipo}</td>
            <td>${row.Equipo_Local}</td>
            <td>${row.Goles_Local ?? '-'} - ${row.Goles_Visitante ?? '-'}</td>
            <td>${row.Equipo_Visitante}</td>
            <td><strong>${row.Puntos}</strong></td>
        `;
        tbody.appendChild(tr);
    });

    summary.innerHTML = `Total Points: ${totalPoints}`;
}
