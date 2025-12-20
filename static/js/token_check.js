// Token geçerlilik kontrolü
function checkTokenExpiry() {
    const token = localStorage.getItem('authToken');
    if (!token) {
        return { valid: false, reason: 'Token bulunamadı' };
    }
    
    try {
        // JWT token'ı decode et (signature doğrulaması yapmadan)
        const parts = token.split('.');
        if (parts.length !== 3) {
            return { valid: false, reason: 'Geçersiz token formatı' };
        }
        
        const payload = JSON.parse(atob(parts[1]));
        const now = Math.floor(Date.now() / 1000);
        
        if (payload.exp && payload.exp < now) {
            return { 
                valid: false, 
                reason: 'Token süresi dolmuş',
                expired: true,
                expiredAt: new Date(payload.exp * 1000).toLocaleString('tr-TR')
            };
        }
        
        return { 
            valid: true, 
            payload: payload,
            expiresAt: payload.exp ? new Date(payload.exp * 1000).toLocaleString('tr-TR') : 'Bilinmiyor'
        };
    } catch (error) {
        return { valid: false, reason: 'Token decode edilemedi: ' + error.message };
    }
}

// Konsola token bilgilerini yazdır
console.log('Token Durumu:', checkTokenExpiry());

