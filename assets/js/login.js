// login.js
// Centraliza la lógica de comprobación de usuario con bcryptjs para reutilización

const login = {
  // Enum-like static roles
  ROLES: {
    ADMINISTRATOR: 'administrator',
    USER: 'user',
    VIP: 'VIP'
  },

  /**
   * Comprueba si el usuario tiene el rol especificado
   * @param {string} username - Nombre de usuario
   * @param {string} roleId - Identificador del rol
   * @returns {Promise<boolean>} true si tiene el rol, false si no
   */
  async hasRole(username, roleId) {
    try {
      const usersData = await fetch('assets/users.json').then(r => r.json());
      if (!usersData || !Array.isArray(usersData.users)) return false;
      const user = usersData.users.find(u => u.name === username);
      if (!user || !Array.isArray(user.role)) return false;
      return user.role.includes(roleId);
    } catch (e) {
      return false;
    }
  },
  
  /**
   * Comprueba la autenticación del usuario y opcionalmente el rol requerido
   * @param {string} user_name - Nombre de usuario
   * @param {string} user_pass - Contraseña del usuario
   * @param {string|null} requiredRole - Rol requerido (opcional)
   * @returns {Promise<void>} Redirige a login.html si falla la autenticación o el rol
   */
  async checkUserAuth(user_name, user_pass, requiredRole = null) {
    if (!user_name || !user_pass) {
      window.location.href = 'login.html';
      return;
    }
    try {
      // Buscar usuario en users.json
      const usersData = await fetch('assets/users.json').then(r => r.json());
      if (!usersData || !Array.isArray(usersData.users)) throw new Error('No users');
      const user = usersData.users.find(u => u.name === user_name);
      if (!user) throw new Error('No user');
      // Esperar a que bcryptjs esté disponible
      function waitForBcrypt() {
        return new Promise(resolve => {
          (function check() {
            if (window.dcodeIO && window.dcodeIO.bcrypt) resolve(window.dcodeIO.bcrypt);
            else if (window.bcryptjs) resolve(window.bcryptjs);
            else if (window.bcrypt) resolve(window.bcrypt);
            else setTimeout(check, 50);
          })();
        });
      }
      const bcrypt = await waitForBcrypt();
      if (!bcrypt.compareSync(user_pass, user.password_hash)) throw new Error('Bad pass');
      
      // Verificar rol requerido si se especifica
      if (requiredRole && Array.isArray(user.role) && !user.role.includes(requiredRole)) {
        throw new Error('Insufficient role');
      }
    } catch (e) {
      window.location.href = 'login.html';
    }
  }
};
