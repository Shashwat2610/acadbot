/**
 * index.js — Entry point for index.html
 * Wires theme + chat modules to the page.
 */

import { initTheme, toggleTheme } from './theme.js';
import {
  initChat,
  openChat,
  closeChat,
  toggleChat,
  sendMessage,
  sendQuery,
  askTopic,
  switchTab,
  clearChat,
  exportChat,
} from './chat.js';

// Initialise on DOM ready
initTheme();
initChat();

// Expose functions globally so inline HTML onclick attributes work seamlessly
window.toggleTheme = toggleTheme;
window.openChat    = openChat;
window.closeChat   = closeChat;
window.toggleChat  = toggleChat;
window.sendMessage = sendMessage;
window.sendQ       = sendQuery;
window.askT        = askTopic;
window.switchTab   = switchTab;
window.clearChat   = clearChat;
window.exportChat  = exportChat;
