export function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast show ${type}`; 
    setTimeout(() => {
    toast.className = 'toast';
    }, 3000);
}