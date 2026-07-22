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

// Global SweetAlert Delete Confirmation
window.confirmDelete = function(event, form, title, text) {
    event.preventDefault();
    Swal.fire({
        title: title || 'Apakah Anda yakin?',
        text: text || 'Data yang dihapus tidak dapat dikembalikan!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#6b7280',
        confirmButtonText: 'Ya, Hapus!',
        cancelButtonText: 'Batal',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            form.submit();
        }
    });
};
