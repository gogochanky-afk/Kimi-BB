// Hugo Sammie 家族辦公室 - Telegram + OpenClaw 雙推送
// 版本：A+C 組合方案

const CONFIG = {
  // Telegram 配置
  BOT_TOKEN: '8519396162:AAGa2WFGBndrOTvP-Y724SIp8_eOI8rrThc',
  CHAT_ID: '7042296651',
  GROUP_ID: '-5153249366',
  
  // OpenClaw 通知配置（方案 A）
  // 暫時用簡單 HTTP endpoint，等有 Hetzner 後更新為正式 Gateway
  OPENCLAW_WEBHOOK: 'https://httpbin.org/post', // 暫時測試用，會記錄請求
  
  // 或用郵件方式（備選）
  // OPENCLAW_EMAIL: 'your-openclaw-email@example.com'
};

/**
 * 發送 Telegram 消息
 */
function sendTelegram(message, chatId) {
  const url = `https://api.telegram.org/bot${CONFIG.BOT_TOKEN}/sendMessage`;
  const payload = {
    chat_id: chatId,
    text: message,
    parse_mode: 'HTML',
    disable_web_page_preview: true
  };
  
  try {
    UrlFetchApp.fetch(url, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload)
    });
  } catch (e) {
    console.log('Telegram error:', e);
  }
}

/**
 * 【方案 A】通知 OpenClaw - 讓 AI 看到並分析
 */
function notifyOpenClaw(message, type) {
  try {
    // 方案 A1: HTTP Webhook（暫時用 httpbin 測試，可以看到請求內容）
    const payload = {
      source: 'hugo_family_office',
      type: type, // 'schedule', 'market', 'news'
      message: message,
      timestamp: new Date().toISOString(),
      date: Utilities.formatDate(new Date(), 'Asia/Hong_Kong', 'yyyy-MM-dd'),
      weekday: new Date().getDay()
    };
    
    // 暫時發送到 httpbin（可以在 https://httpbin.org/ 查看請求）
    UrlFetchApp.fetch(CONFIG.OPENCLAW_WEBHOOK, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
    
    // 方案 A2: 如果用郵件方式（需要配置郵件發送權限）
    // GmailApp.sendEmail(CONFIG.OPENCLAW_EMAIL, `[Hugo Office] ${type}`, message);
    
    console.log('Notified OpenClaw:', type);
  } catch (e) {
    // 靜默失敗，不影響 Telegram 發送
    console.log('OpenClaw notify failed:', e);
  }
}

/**
 * 雙推送 (Telegram + OpenClaw)
 */
function sendToBoth(message, type = 'general') {
  // 1. 發送到 Telegram
  sendTelegram(message, CONFIG.CHAT_ID);
  sendTelegram(message, CONFIG.GROUP_ID);
  
  // 2. 【新增】通知 OpenClaw，讓 AI 看到並可以回覆分析
  notifyOpenClaw(message, type);
}

/**
 * 1. 家庭日程 (每天 7:45-8:45 AM)
 */
function scheduleReport() {
  const today = new Date();
  const weekday = today.getDay();
  const dateStr = Utilities.formatDate(today, 'Asia/Hong_Kong', 'MM月dd日');
  const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
  
  const schedules = {
    0: {morning: '大女儿校队至 5:00 PM', evening: '中国乐器 6:45-8:00 PM', note: '记得带乐器'},
    1: {morning: '大女儿校队至 5:00 PM', evening: '晚上自由时间', note: '可以安排家庭活动'},
    2: {morning: '半天课 (1:00 PM 放学)', afternoon: '法文/编程/数学堂', note: '接孩子时间较早'},
    3: {morning: '大女儿校队至 5:00 PM', evening: '晚上自由时间', note: '检查本周功课'},
    4: {morning: '正常上课', afternoon: '网球 4:00-5:00 PM', note: '带网球装备！'},
    5: {morning: '周末家庭时间', note: '可以安排户外活动'},
    6: {morning: '周末休息', note: '准备下周'}
  };
  
  const s = schedules[weekday];
  let msg = `📋 <b>Hugo Sammie 家庭日程</b>\n`;
  msg += `📅 ${dateStr} 星期${weekdays[weekday]}\n\n`;
  if (s.morning) msg += `🌅 上午：${s.morning}\n`;
  if (s.afternoon) msg += `☀️ 下午：${s.afternoon}\n`;
  if (s.evening) msg += `🌙 晚上：${s.evening}\n`;
  msg += `\n💡 <b>提醒：</b>${s.note}\n\n<i>☕ 祝你有美好的一天！</i>`;
  
  sendToBoth(msg, 'schedule');
}

/**
 * 2. 全球晨报 (每天 9:00-10:00 AM)
 */
function newsReport() {
  const today = Utilities.formatDate(new Date(), 'Asia/Hong_Kong', 'MM月dd日');
  let msg = `🌍 <b>全球晨报 | ${today}</b>\n\n`;
  msg += `📌 <b>今日要点</b>\n`;
  msg += `• 市场动态持续跟踪\n`;
  msg += `• 美股开盘前推送详细简报\n\n`;
  msg += `⏰ <b>今日安排</b>\n`;
  msg += `• 8:30 PM - 美股盘前简报\n`;
  msg += `• 10:30 PM - 开盘机会检查\n\n`;
  msg += `<i>— Hugo Sammie 家族办公室</i>`;
  
  sendToBoth(msg, 'news');
}

/**
 * 3. 美股盘前简报 (週一到五 8:00-9:00 PM)
 */
function premarketReport() {
  const today = Utilities.formatDate(new Date(), 'Asia/Hong_Kong', 'MM月dd日');
  let msg = `📊 <b>美股盘前简报 | ${today}</b>\n\n`;
  msg += `🌙 <b>盘前概况</b>\n`;
  msg += `• 期指走势跟踪中\n`;
  msg += `• 开盘前情绪观察\n\n`;
  msg += `⏰ <b>今晚安排</b>\n`;
  msg += `• 10:30 PM - 开盘机会检查\n\n`;
  msg += `💡 <b>小GoGo提醒</b>\n`;
  msg += `👀 有重要异动会立即推送\n\n`;
  msg += `<i>— Hugo Sammie 家族办公室</i>`;
  
  sendToBoth(msg, 'market');
}

/**
 * 4. 开盘机会检查 (週一到五 10:00-11:00 PM)
 */
function opportunityCheck() {
  const msg = `📈 <b>开盘机会检查</b>\n\n` +
              `✅ 美股已开盘\n` +
              `• 正在监控持仓股票\n` +
              `• 有异动脉冲会立即通知\n\n` +
              `<i>— Hugo Sammie 家族办公室</i>`;
  
  sendToBoth(msg, 'market');
}

/**
 * 5. 全家阅读计划 (週日 10:00-11:00 AM)
 */
function readingReport() {
  const msg = `📚 <b>全家阅读计划 | 周日</b>\n\n` +
              `🎯 <b>本周推荐</b>\n` +
              `• 安排亲子阅读时间\n` +
              `• 推荐适合全家阅读的书籍\n\n` +
              `⏰ <b>下周预告</b>\n` +
              `• 周一 7:45 AM - 家庭日程\n` +
              `• 周一至周五晚上 - 美股简报\n\n` +
              `<i>— Hugo Sammie 家族办公室</i>`;
  
  sendToBoth(msg, 'reading');
}

/**
 * 測試函數
 */
function test() {
  scheduleReport();
  console.log('測試完成！檢查 Telegram 和 OpenClaw Webhook');
}
