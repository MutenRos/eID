// eID - JavaScript principal

// Actualizar contador de mensajes no leídos
function updateUnreadCount() {
    fetch('/chat/unread-count')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('unread-badge');
            if (badge && data.count > 0) {
                badge.textContent = data.count;
                badge.style.display = 'inline';
            } else if (badge) {
                badge.style.display = 'none';
            }
        })
        .catch(error => console.error('Error:', error));
}

// Actualizar cada 5 segundos si el usuario está autenticado
if (document.getElementById('unread-badge')) {
    updateUnreadCount();
    setInterval(updateUnreadCount, 5000);
}

// Búsqueda de usuarios (para la página de contactos)
function searchUsers(query) {
    if (query.length < 2) {
        document.getElementById('search-results').innerHTML = '';
        return;
    }
    
    fetch(`/contacts/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(users => {
            const resultsDiv = document.getElementById('search-results');
            if (users.length === 0) {
                resultsDiv.innerHTML = '<p>No se encontraron usuarios</p>';
                return;
            }
            
            resultsDiv.innerHTML = users.map(user => `
                <div class="user-result">
                    <img src="/static/img/${user.avatar}" alt="${user.username}">
                    <div>
                        <strong>${user.username}</strong>
                        ${user.full_name ? `<br><small>${user.full_name}</small>` : ''}
                    </div>
                    <form method="POST" action="/contacts/add/${user.id}" style="display:inline">
                        <button type="submit" class="btn btn-primary">Agregar</button>
                    </form>
                </div>
            `).join('');
        })
        .catch(error => console.error('Error:', error));
}

// Auto-cerrar alertas después de 5 segundos
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// Scroll suave para el chat (mantener al final al cargar)
const chatMessages = document.getElementById('chat-messages');
if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
