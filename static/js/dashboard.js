// Toggle Sidebar
const toggleSidebar = () => {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('hidden');
  };
  
  document.querySelector('.header h2').addEventListener('click', toggleSidebar);
  