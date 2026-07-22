// Custom JS untuk inisialisasi awal atau utility
document.addEventListener('alpine:init', () => {
    // Registrasi store atau komponen Alpine JS jika dibutuhkan secara global
    
    // Contoh format currency IDR
    Alpine.data('utils', () => ({
        formatRupiah(number) {
            return new Intl.NumberFormat('id-ID', {
                style: 'currency',
                currency: 'IDR',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(number);
        }
    }));
});
