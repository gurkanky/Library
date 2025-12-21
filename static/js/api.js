// API Base URL
const API_BASE_URL = 'http://localhost:5000/api';

// Token yönetimi
let authToken = localStorage.getItem('authToken');
let currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null');

// API Helper Functions
const api = {
    setToken(token) {
        authToken = token;
        localStorage.setItem('authToken', token);
    },
    getToken() {
        return authToken || localStorage.getItem('authToken');
    },
    setUser(user) {
        currentUser = user;
        localStorage.setItem('currentUser', JSON.stringify(user));
    },
    getUser() {
        return currentUser || JSON.parse(localStorage.getItem('currentUser') || 'null');
    },
    logout() {
        authToken = null;
        currentUser = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('currentUser');
        window.location.href = 'index.html'; // Login sayfasına yönlendir
    },
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const token = this.getToken();
        const defaultOptions = {
            headers: { 'Content-Type': 'application/json' }
        };
        if (token) {
            defaultOptions.headers['Authorization'] = `Bearer ${token}`;
        }
        const config = {
            ...defaultOptions,
            ...options,
            headers: { ...defaultOptions.headers, ...(options.headers || {}) }
        };
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            if (response.status === 401) {
                this.logout();
                throw new Error('Oturum süresi dolmuş.');
            }
            if (!response.ok) {
                throw new Error(data.message || 'Bir hata oluştu');
            }
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    async get(endpoint) { return this.request(endpoint, { method: 'GET' }); },
    async post(endpoint, data) { return this.request(endpoint, { method: 'POST', body: JSON.stringify(data) }); },
    async put(endpoint, data) { return this.request(endpoint, { method: 'PUT', body: JSON.stringify(data) }); },
    async delete(endpoint) { return this.request(endpoint, { method: 'DELETE' }); }
};

// --- API GRUPLARI ---

const authAPI = {
    async register(userData) { return api.post('/auth/register', userData); },
    async login(email, password) { return api.post('/auth/login', { eposta: email, sifre: password }); },
    async getCurrentUser() { return api.get('/auth/me'); }
};

const bookAPI = {
    async getAll(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return api.get(`/books${queryString ? '?' + queryString : ''}`);
    },
    async getById(bookId) { return api.get(`/books/${bookId}`); },
    async create(bookData) { return api.post('/books', bookData); },
    async update(bookId, bookData) { return api.put(`/books/${bookId}`, bookData); },
    async delete(bookId) { return api.delete(`/books/${bookId}`); }
};

const borrowAPI = {
    async borrow(bookId, days = 21) { return api.post('/borrow', { kitapID: bookId, oduncGunSayisi: days }); },
    async returnBook(borrowId) { return api.post(`/borrow/${borrowId}/return`, {}); },
    async getMyBooks() { return api.get('/borrow/my-books'); },
    async getAll() { return api.get('/borrow/all'); },
    async getOverdue() { return api.get('/borrow/overdue'); },
    async checkOverdue() { return api.post('/borrow/check-overdue'); }
};

const categoryAPI = {
    async getAll() { return api.get('/categories'); },
    async getById(categoryId) { return api.get(`/categories/${categoryId}`); },
    async create(categoryData) { return api.post('/categories', categoryData); },
    async update(categoryId, categoryData) { return api.put(`/categories/${categoryId}`, categoryData); },
    async delete(categoryId) { return api.delete(`/categories/${categoryId}`); }
};

const authorAPI = {
    async getAll(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return api.get(`/authors${queryString ? '?' + queryString : ''}`);
    },
    async getById(authorId) { return api.get(`/authors/${authorId}`); },
    async create(authorData) { return api.post('/authors', authorData); },
    async update(authorId, authorData) { return api.put(`/authors/${authorId}`, authorData); },
    async delete(authorId) { return api.delete(`/authors/${authorId}`); }
};

const userAPI = {
    async getProfile() { return api.get('/users/profile'); },
    async getPenalties() { return api.get('/users/penalties'); },
    async getDebt() { return api.get('/users/debt'); },
    async payPenalty(penaltyId) { return api.post(`/users/penalties/${penaltyId}/pay`); },

    // --- YENİ EKLENEN FAVORİ METODLARI ---
    async getFavorites() { return api.get('/users/favorites'); },
    async addFavorite(bookId) { return api.post(`/users/favorites/${bookId}`); },
    async removeFavorite(bookId) { return api.delete(`/users/favorites/${bookId}`); }
};

const adminAPI = {
    async getAllUsers() { return api.get('/admin/users'); },
    async updateUser(userId, userData) { return api.put(`/admin/users/${userId}`, userData); },
    async deleteUser(userId) { return api.delete(`/admin/users/${userId}`); },
    async getAllPenalties() { return api.get('/admin/penalties'); },
    async getStatistics() { return api.get('/admin/statistics'); }
};

// YENİ EKLENEN KISIM:
const reservationAPI = {
    async create(reservationData) { return api.post('/reservations', reservationData); },
    async getMyReservations() { return api.get('/reservations/my-reservations'); },
    async cancel(reservationId) { return api.post(`/reservations/${reservationId}/cancel`); }
};

// Review API
const reviewAPI = {
    async getByBook(bookId) {
        return api.get(`/reviews/book/${bookId}`);
    },
    async add(data) {
        return api.post('/reviews', data);
    },
    async delete(reviewId) {
        return api.delete(`/reviews/${reviewId}`);
    }
};