// Authentication functions

// Sayfa yüklendiğinde kontrol et
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    setupAuthForms();
});

function checkAuth() {
    if (typeof api === 'undefined') return;

    const token = api.getToken();
    const user = api.getUser();

    // Eğer dashboard gibi korumalı bir sayfadaysak ve token yoksa yönlendirme yapılabilir
    // Ancak login/register sayfalarında bu kontrol farklı çalışmalı.

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

    // Verification form (Register sayfasında)
    const verificationForm = document.getElementById('verificationForm');
    if (verificationForm) {
        verificationForm.addEventListener('submit', handleVerify);
    }

    // YENİ: Forgot Password Form
    const forgotForm = document.getElementById('forgotPasswordForm');
    if (forgotForm) {
        forgotForm.addEventListener('submit', handleForgotPassword);
    }

    // YENİ: Reset Password Form
    const resetForm = document.getElementById('resetPasswordForm');
    if (resetForm) {
        resetForm.addEventListener('submit', handleResetPassword);
    }
}

// --- HANDLERS ---

async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        showLoading('Giriş yapılıyor...');
        const result = await authAPI.login(email, password);

        if (result.success && result.access_token) {
            loginSuccess(result);
        } else {
            throw new Error(result.message || 'Giriş başarısız');
        }
    } catch (error) {
        showAlert(error.message || 'Giriş başarısız!', 'danger');
    } finally {
        hideLoading();
    }
}

async function handleRegister(e) {
    e.preventDefault();

    const emailInput = document.getElementById('registerEmail');
    const formData = {
        ad: document.getElementById('registerAd').value,
        soyad: document.getElementById('registerSoyad').value,
        eposta: emailInput.value,
        sifre: document.getElementById('registerPassword').value,
        telefon: document.getElementById('registerTelefon').value,
        adres: document.getElementById('registerAdres').value
    };

    try {
        showLoading('Kayıt yapılıyor...');
        const result = await authAPI.register(formData);

        if (result.success && result.require_verification) {
            showAlert(result.message, 'success');

            // Kayıt formunu gizle, doğrulama formunu göster
            document.getElementById('registerForm').style.display = 'none';
            document.getElementById('verificationForm').style.display = 'block';

            // E-postayı doğrulama formuna taşı
            document.getElementById('verifyEmail').value = formData.eposta;

            // Başlığı güncelle
            const header = document.querySelector('.card-header');
            if(header) header.textContent = "Hesap Doğrulama";

        } else if (result.success && result.access_token) {
            loginSuccess(result);
        } else {
            throw new Error(result.message || 'Kayıt başarısız');
        }
    } catch (error) {
        showAlert(error.message || 'Kayıt başarısız!', 'danger');
    } finally {
        hideLoading();
    }
}

async function handleVerify(e) {
    e.preventDefault();

    const email = document.getElementById('verifyEmail').value;
    const code = document.getElementById('verifyCode').value;

    try {
        showLoading('Kod doğrulanıyor...');
        const result = await authAPI.verifyEmail({
            eposta: email,
            kod: code
        });

        if (result.success) {
            showAlert('Hesabınız başarıyla doğrulandı! Giriş sayfasına yönlendiriliyorsunuz...', 'success');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            throw new Error(result.message || 'Doğrulama başarısız');
        }
    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        hideLoading();
    }
}

// YENİ: Şifremi Unuttum Handler
async function handleForgotPassword(e) {
    e.preventDefault();
    const email = document.getElementById('forgotEmail').value;

    try {
        showLoading('Kod gönderiliyor...');
        const result = await authAPI.forgotPassword(email);

        if (result.success) {
            // E-postayı sonraki sayfada kullanmak için sakla
            localStorage.setItem('reset_email', email);
            showAlert(result.message, 'success');
            setTimeout(() => {
                window.location.href = 'reset-password.html';
            }, 1500);
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('Bir hata oluştu: ' + error.message, 'danger');
    } finally {
        hideLoading();
    }
}

// YENİ: Şifre Sıfırlama Handler
async function handleResetPassword(e) {
    e.preventDefault();

    const email = document.getElementById('resetEmail').value;
    const code = document.getElementById('resetCode').value;
    const pass1 = document.getElementById('newPassword').value;
    const pass2 = document.getElementById('newPasswordConfirm').value;

    if (pass1 !== pass2) {
        showAlert('Şifreler eşleşmiyor!', 'warning');
        return;
    }

    try {
        showLoading('Şifre güncelleniyor...');
        const result = await authAPI.resetPassword({
            eposta: email,
            kod: code,
            yeni_sifre: pass1
        });

        if (result.success) {
            localStorage.removeItem('reset_email');
            showAlert('Şifreniz başarıyla değiştirildi! Giriş sayfasına yönlendiriliyorsunuz...', 'success');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('Hata: ' + error.message, 'danger');
    } finally {
        hideLoading();
    }
}

// --- HELPERS ---

function loginSuccess(result) {
    api.setToken(result.access_token);
    api.setUser(result.user);
    console.log('Giriş başarılı');
    showAlert('Giriş başarılı! Yönlendiriliyorsunuz...', 'success');

    setTimeout(() => {
        window.location.href = 'dashboard.html';
    }, 1000);
}

function logout() {
    if (confirm('Çıkış yapmak istediğinize emin misiniz?')) {
        api.logout();
    }
}

function showAlert(message, type = 'info') {
    const oldAlert = document.querySelector('.alert-notification');
    if (oldAlert) oldAlert.remove();

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-notification`;
    alertDiv.textContent = message;

    const container = document.querySelector('.card') || document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);

        const duration = type === 'danger' ? 8000 : 5000;
        setTimeout(() => {
            alertDiv.remove();
        }, duration);
    }
}

function showLoading(message = 'Yükleniyor...') {
    hideLoading();
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