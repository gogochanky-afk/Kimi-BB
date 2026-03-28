// Hugo Sammie 家族辦公室 - 智能版 (周末自動跳過股市通知)
// 版本：v3_smart - 只在工作日發送股市相關通知

const CONFIG = {
  BOT_TOKEN: '8519396162:AAGa2WFGBndrOTvP-Y724SIp8_eOI8rrThc',
  CHAT_ID: '7042296651',
  GROUP_ID: '-5153249366'
};

/**
 * 檢查是否工作日 (周一到周五)
 */
function isWeekday() {
  const day = new Date().getDay(); // 0=周日, 1=周一, ..., 6=周六
  return day >= 1 && day <= 5; // 周一到周五
}

/**
 * 檢查是否周末
 */
function isWeekend() {
  return !isWeekday();
}

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
 * 發送到 Telegram (私人和群組)
 */
function sendToBoth(message) {
  sendTelegram(message, CONFIG.CHAT_ID);
  sendTelegram(message, CONFIG.GROUP_ID);
}

/**
 * 1. 家庭日程 (每天發送 - 包含周末)
 */
function scheduleReport() {
  const today = new Date();
  const weekday = today.getDay();
  const dateStr = Utilities.formatDate(today, 'Asia/Hong_Kong', 'MM月dd日');
  const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
  
  const schedules = {
    0: {morning: '周末休息', note: '准备下周，晚上有阅读计划'},
    1: {morning: '大女儿校队至 5:00 PM', evening: '中国乐器 6:45-8:00 PM', note: '记得带乐器'},
    2: {morning: '大女儿校队至 5:00 PM', evening: '晚上自由时间', note: '可以安排家庭活动'},
    3: {morning: '半天课 (1:00 PM 放学)', afternoon: '法文/编程/数学堂', note: '接孩子时间较早'},
    4: {morning: '大女儿校队至 5:00 PM', evening: '晚上自由时间', note: '检查本周功课'},
    5: {morning: '正常上课', afternoon: '网球 4:00-5:00 PM', note: '带网球装备！'},
    6: {morning: '周末家庭时间', note: '可以安排户外活动'}
  };
  
  const s = schedules[weekday];
  let msg = `📋 <b>Hugo Sammie 家庭日程</b>\n`;
  msg += `📅 ${dateStr} 星期${weekdays[weekday]}\n\n`;
  if (s.morning) msg += `🌅 上午：${s.morning}\n`;
  if (s.afternoon) msg += `☀️ 下午：${s.afternoon}\n`;
  if (s.evening) msg += `🌙 晚上：${s.evening}\n`;
  msg += `\n💡 <b>提醒：</b>${s.note}\n\n<i>☕ 祝你有美好的一天！</i>`;
  
  sendToBoth(msg);
}

/**
 * 2. 全球晨报 (工作日發送 / 周末發送家庭版)
 */
function newsReport() {
  const today = Utilities.formatDate(new Date(), 'Asia/Hong_Kong', 'MM月dd日');
  
  if (isWeekend()) {
    // 周末：發送家庭版，不發股市
    let msg = `🏠 <b>周末家庭简报 | ${today}</b>\n\n`;
    msg += `📌 <b>今日安排</b>\n`;
    msg += `• 享受家庭时光\n`;
    msg += `• 美股休市，无市场动态\n`;
    msg += `• 周日 10:00 AM 有阅读计划\n\n`;
    msg += `<i>— Hugo Sammie 家族办公室</i>`;
    sendToBoth(msg);
  } else {
    // 工作日：發送股市版
    let msg = `🌍 <b>全球晨报 | ${today}</b>\n\n`;
    msg += `📌 <b>今日要点</b>\n`;
    msg += `• 市场动态持续跟踪\n`;
    msg += `• 美股开盘前推送详细简报\n\n`;
    msg += `⏰ <b>今日安排</b>\n`;
    msg += `• 8:30 PM - 美股盘前简报\n`;
    msg += `• 10:30 PM - 开盘机会检查\n\n`;
    msg += `<i>— Hugo Sammie 家族办公室</i>`;
    sendToBoth(msg);
  }
}

/**
 * 3. 美股盘前简报 (只工作日發送)
 */
function premarketReport() {
  // 🔴 周末自動跳過
  if (isWeekend()) {
    console.log('周末美股休市，跳过盘前简报');
    return;
  }
  
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
  
  sendToBoth(msg);
}

/**
 * 4. 开盘机会检查 (只工作日發送)
 */
function opportunityCheck() {
  // 🔴 周末自動跳過
  if (isWeekend()) {
    console.log('周末美股休市，跳过机会检查');
    return;
  }
  
  const msg = `📈 <b>开盘机会检查</b>\n\n` +
              `✅ 美股已开盘\n` +
              `• 正在监控持仓股票\n` +
              `• 有异动脉冲会立即通知\n\n` +
              `<i>— Hugo Sammie 家族办公室</i>`;
  
  sendToBoth(msg);
}

/**
 * 5. 全家阅读计划 (只周日發送)
 */
function readingReport() {
  const weekday = new Date().getDay();
  
  // 只在周日發送
  if (weekday !== 0) {
    console.log('不是周日，跳过阅读计划');
    return;
  }
  
  const msg = `📚 <b>全家阅读计划 | 周日</b>\n\n` +
              `🎯 <b>本周推荐</b>\n` +
              `• 安排亲子阅读时间\n` +
              `• 推荐适合全家阅读的书籍\n\n` +
              `⏰ <b>下周预告</b>\n` +
              `• 周一 7:45 AM - 家庭日程\n` +
              `• 周一至周五晚上 - 美股简报\n\n` +
              `<i>— Hugo Sammie 家族办公室</i>`;
  
  sendToBoth(msg);
}

/**
 * 測試函數
 */
function test() {
  console.log('今天是星期:', new Date().getDay());
  console.log('是否工作日:', isWeekday());
  
  scheduleReport();
  
  if (isWeekday()) {
    console.log('工作日，测试股市通知...');
    newsReport();
    premarketReport();
  } else {
    console.log('周末，股市通知已跳过');
  }
}

/**
 * 測試周末跳過功能
 */
function testWeekendSkip() {
  console.log('=== 測試智能過濾功能 ===');
  console.log('今天星期:', new Date().getDay());
  console.log('工作日?', isWeekday());
  console.log('周末?', isWeekend());
  
  // 模擬調用
  console.log('\n調用 premarketReport()...');
  premarketReport();
  
  console.log('\n調用 opportunityCheck()...');
  opportunityCheck();
  
  console.log('\n調用 readingReport()...');
  readingReport();
}
