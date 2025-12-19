// Authentication functions

// Sayfa yüklendiğinde kontrol et
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    setupAuthForms();
});

function checkAuth() {
    const token = api.getToken();
    const user = api.getUser();
    
    if (token && user) {
        updateUserInfo(user);
        showAuthenticatedContent();
    } else {
        showUnauthenticatedContent();
    }
}

function showAuthenticatedContent() {
    const authLinks = document.querySelectorAll('.auth-link');
    const userLinks = document.querySelectorAll('.user-link');
    
    authLinks.forEach(link => link.style.display = 'none');
    userLinks.forEach(link => link.style.display = 'block');
}

function showUnauthenticatedContent() {
    const authLinks = document.querySelectorAll('.auth-link');
    const userLinks = document.querySelectorAll('.user-link');
    
    authLinks.forEach(link => link.style.display = 'block');
    userLinks.forEach(link => link.style.display = 'none');
}

function updateUserInfo(user) {
    const userInfoElements = document.querySelectorAll('.user-info-text');
    userInfoElements.forEach(el => {
        if (user) {
            el.textContent = `${user.ad} ${user.soyad} (${user.rol})`;
        }
    });
}

function setupAuthForms() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
}

async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        showLoading('Giriş yapılıyor...');
        const result = await authAPI.login(email, password);
        
        if (result.success) {
            api.setToken(result.access_token);
            api.setUser(result.user);
            showAlert('Giriş başarılı!', 'success');
            
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        }
    } catch (error) {
        showAlert(error.message || 'Giriş başarısız!', 'danger');
    } finally {
        hideLoading();
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const formData = {
        ad: document.getElementById('registerAd').value,
        soyad: document.getElementById('registerSoyad').value,
        eposta: document.getElementById('registerEmail').value,
        sifre: document.getElementById('registerPassword').value,
        telefon: document.getElementById('registerTelefon').value,
        adres: document.getElementById('registerAdres').value
    };
    
    try {
        showLoading('Kayıt yapılıyor...');
        const result = await authAPI.register(formData);
        
        if (result.success) {
            api.setToken(result.access_token);
            api.setUser(result.user);
            showAlert('Kayıt başarılı!', 'success');
            
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        }
    } catch (error) {
        showAlert(error.message || 'Kayıt başarısız!', 'danger');
    } finally {
        hideLoading();
    }
}

function logout() {
    if (confirm('Çıkış yapmak istediğinize emin misiniz?')) {
        api.logout();
    }
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

function showLoading(message = 'Yükleniyor...') {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading';
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = `
        <div class="spinner"></div>
        <p>${message}</p>
    `;
    
    document.body.appendChild(loadingDiv);
}

function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.remove();
    }
}

