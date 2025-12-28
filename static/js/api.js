// API Base URL
const API_BASE_URL = '';

// --- GENEL YARDIMCILAR ---
const api = {
    getToken: () => localStorage.getItem('access_token'),
    setToken: (token) => localStorage.setItem('access_token', token),
    removeToken: () => localStorage.removeItem('access_token'),

    getUser: () => {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },
    setUser: (user) => localStorage.setItem('user', JSON.stringify(user)),
    removeUser: () => localStorage.removeItem('user'),

    logout: () => {
        api.removeToken();
        api.removeUser();
        window.location.href = 'login.html';
    },

    // Standart Fetch Fonksiyonu
    fetch: async (endpoint, options = {}) => {
        const token = api.getToken();

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        let url = `${API_BASE_URL}${endpoint}`;
        if (options.params) {
            const params = new URLSearchParams(options.params);
            url += `?${params.toString()}`;
        }

        const config = {
            method: options.method || 'GET',
            headers: headers,
        };

        if (options.body) {
            config.body = typeof options.body === 'string' ? options.body : JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, config);

            if (response.status === 401) {
                console.warn('Oturum süresi doldu.');
                api.logout();
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error('API Hatası:', error);
            throw error;
        }
    }
};

// --- 1. AUTH (KİMLİK DOĞRULAMA) API ---
const authAPI = {
    login: async (email, password) => {
        return await api.fetch('/api/auth/login', {
            method: 'POST',
            body: { eposta: email, sifre: password }
        });
    },
    register: async (userData) => {
        return await api.fetch('/api/auth/register', {
            method: 'POST',
            body: userData
        });
    },
    verifyEmail: async (data) => {
        return await api.fetch('/api/auth/verify-email', {
            method: 'POST',
            body: data
        });
    },
    getCurrentUser: async () => {
        return await api.fetch('/api/auth/me');
    },
    forgotPassword: async (email) => {
        return await api.fetch('/api/auth/forgot-password', {
            method: 'POST',
            body: { eposta: email }
        });
    },
    resetPassword: async (data) => {
        return await api.fetch('/api/auth/reset-password', {
            method: 'POST',
            body: data
        });
    }
};

// --- 2. KİTAP (BOOK) API ---
const bookAPI = {
    getAll: async (params = {}) => {
        return await api.fetch('/api/books', { params });
    },
    getById: async (id) => {
        return await api.fetch(`/api/books/${id}`);
    },
    create: async (data) => {
        return await api.fetch('/api/books', {
            method: 'POST',
            body: data
        });
    },
    update: async (id, data) => {
        return await api.fetch(`/api/books/${id}`, {
            method: 'PUT',
            body: data
        });
    },
    delete: async (id) => {
        return await api.fetch(`/api/books/${id}`, {
            method: 'DELETE'
        });
    }
};

// --- 3. KATEGORİ API ---
const categoryAPI = {
    getAll: async () => {
        return await api.fetch('/api/categories');
    }
};

// --- 4. ÖDÜNÇ (BORROW) API ---
const borrowAPI = {
    getMyBooks: async () => {
        return await api.fetch('/api/borrow/my-books');
    },
    borrow: async (bookId) => {
        return await api.fetch('/api/borrow', {
            method: 'POST',
            body: { kitapID: bookId }
        });
    },
    returnBook: async (borrowId) => {
        return await api.fetch(`/api/borrow/${borrowId}/return`, {
            method: 'POST'
        });
    },
    getAll: async () => {
        return await api.fetch('/api/borrow/all');
    },
    getOverdue: async () => {
        return await api.fetch('/api/borrow/overdue');
    },
    checkOverdue: async () => {
        return await api.fetch('/api/borrow/check-overdue', {
            method: 'POST'
        });
    }
};

// --- 5. KULLANICI (USER) API ---
const userAPI = {
    getProfile: async () => {
        return await api.fetch('/api/users/profile');
    },
    getDebt: async () => {
        return await api.fetch('/api/users/debt');
    },
    getPenalties: async () => {
        return await api.fetch('/api/users/penalties');
    },
    payPenalty: async (penaltyId) => {
        return await api.fetch(`/api/users/penalties/${penaltyId}/pay`, {
            method: 'POST'
        });
    },
    addFavorite: async (bookId) => {
        return await api.fetch(`/api/users/favorites/${bookId}`, {
            method: 'POST'
        });
    },
    removeFavorite: async (bookId) => {
        return await api.fetch(`/api/users/favorites/${bookId}`, {
            method: 'DELETE'
        });
    },
    getFavorites: async () => {
        return await api.fetch('/api/users/favorites');
    },
    // YENİ EKLENENLER:
    deleteAccount: async () => {
        return await api.fetch('/api/users/delete-account', {
            method: 'DELETE'
        });
    },
    changePassword: async (data) => {
        return await api.fetch('/api/users/change-password', {
            method: 'POST',
            body: data
        });
    }
};

// --- 6. REZERVASYON API ---
const reservationAPI = {
    getMyReservations: async () => {
        return await api.fetch('/api/reservations/my-reservations');
    },
    create: async (data) => {
        return await api.fetch('/api/reservations', {
            method: 'POST',
            body: data
        });
    }
};

// --- 7. YORUM (REVIEW) API ---
const reviewAPI = {
    getByBook: async (bookId) => {
        return await api.fetch(`/api/reviews/book/${bookId}`);
    },
    add: async (data) => {
        return await api.fetch('/api/reviews', {
            method: 'POST',
            body: data
        });
    },
    delete: async (reviewId) => {
        return await api.fetch(`/api/reviews/${reviewId}`, {
            method: 'DELETE'
        });
    }
};

// --- 8. ADMIN API ---
const adminAPI = {
    getStatistics: async () => {
        return await api.fetch('/api/admin/statistics');
    },
    getAllPenalties: async () => {
        return await api.fetch('/api/admin/penalties');
    },
    getUsers: async () => {
        return await api.fetch('/api/admin/users');
    },
    updateUser: async (id, data) => {
        return await api.fetch(`/api/admin/users/${id}`, {
            method: 'PUT',
            body: data
        });
    },
    deleteUser: async (id) => {
        return await api.fetch(`/api/admin/users/${id}`, {
            method: 'DELETE'
        });
    }
};