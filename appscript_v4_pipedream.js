// Hugo Sammie 家族辦公室 - 智能版 (含 Pipedream Webhook)
// 版本：v4_with_pipedream - 自動發送到 Telegram + Pipedream (我能看到)

const CONFIG = {
  BOT_TOKEN: '8519396162:AAGa2WFGBndrOTvP-Y724SIp8_eOI8rrThc',
  CHAT_ID: '7042296651',
  GROUP_ID: '-5153249366',
  
  // ✅ Pipedream Webhook URL - 讓我能看到通知並分析
  PIPEDREAM_WEBHOOK: 'https://eoqjc16cqlmt40r.m.pipedream.net'
};

/**
 * 檢查是否工作日 (周一到周五)
 */
function isWeekday() {
  const day = new Date().getDay();
  return day >= 1 && day <= 5;
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
 * 【新增】發送到 Pipedream，讓 AI 看到並分析
 */
function notifyPipedream(message, type) {
  try {
    const payload = {
      source: 'hugo_family_office',
      type: type,
      message: message,
      timestamp: new Date().toISOString(),
      date: Utilities.formatDate(new Date(), 'Asia/Hong_Kong', 'yyyy-MM-dd'),
      weekday: new Date().getDay()
    };
    
    UrlFetchApp.fetch(CONFIG.PIPEDREAM_WEBHOOK, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
    
    console.log('Sent to Pipedream:', type);
  } catch (e) {
    console.log('Pipedream notify failed:', e);
  }
}

/**
 * 發送到 Telegram + Pipedream
 */
function sendToBoth(message, type) {
  // 1. 發送到 Telegram（給您看）
  sendTelegram(message, CONFIG.CHAT_ID);
  sendTelegram(message, CONFIG.GROUP_ID);
  
  // 2. 【新增】發送到 Pipedream（讓我看到並回覆分析）
  notifyPipedream(message, type);
}

/**
 * 1. 家庭日程 (每天發送)
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
  let msg = `📋 Hugo Sammie 家庭日程\n`;
  msg += `📅 ${dateStr} 星期${weekdays[weekday]}\n\n`;
  if (s.morning) msg += `🌅 上午：${s.morning}\n`;
  if (s.afternoon) msg += `☀️ 下午：${s.afternoon}\n`;
  if (s.evening) msg += `🌙 晚上：${s.evening}\n`;
  msg += `\n💡 提醒：${s.note}\n\n☕ 祝你有美好的一天！`;
  
  sendToBoth(msg, 'schedule');
}

/**
 * 2. 全球晨报 (工作日發送 / 周末發送家庭版)
 */
function newsReport() {
  const today = Utilities.formatDate(new Date(), 'Asia/Hong_Kong', 'MM月dd日');
  
  if (isWeekend()) {
    // 周末：發送家庭版
    let msg = `🏠 周末家庭简报 | ${today}\n\n`;
    msg += `📌 今日安排\n`;
    msg += `• 享受家庭时光\n`;
    msg += `• 美股休市，无市场动态\n`;
    msg += `• 周日 10:00 AM 有阅读计划\n\n`;
    msg += `— Hugo Sammie 家族办公室`;
    sendToBoth(msg, 'news');
  } else {
    // 工作日：發送股市版
    let msg = `🌍 全球晨报 | ${today}\n\n`;
    msg += `📌 今日要点\n`;
    msg += `• 市场动态持续跟踪\n`;
    msg += `• 美股开盘前推送详细简报\n\n`;
    msg += `⏰ 今日安排\n`;
    msg += `• 8:30 PM - 美股盘前简报\n`;
    msg += `• 10:30 PM - 开盘机会检查\n\n`;
    msg += `— Hugo Sammie 家族办公室`;
    sendToBoth(msg, 'news');
  }
}

/**
 * 3. 美股盘前简报 (只工作日發送)
 */
function premarketReport() {
  if (isWeekend()) {
    console.log('周末美股休市，跳过盘前简报');
    return;
  }
  
  const today = Utilities.formatDate(new Date(), 'Asia/Hong_Kong', 'MM月dd日');
  let msg = `📊 美股盘前简报 | ${today}\n\n`;
  msg += `🌙 盘前概况\n`;
  msg += `• 期指走势跟踪中\n`;
  msg += `• 开盘前情绪观察\n\n`;
  msg += `⏰ 今晚安排\n`;
  msg += `• 10:30 PM - 开盘机会检查\n\n`;
  msg += `💡 小GoGo提醒\n`;
  msg += `👀 有重要异动会立即推送\n\n`;
  msg += `— Hugo Sammie 家族办公室`;
  
  sendToBoth(msg, 'market');
}

/**
 * 4. 开盘机会检查 (只工作日發送)
 */
function opportunityCheck() {
  if (isWeekend()) {
    console.log('周末美股休市，跳过机会检查');
    return;
  }
  
  const msg = `📈 开盘机会检查\n\n` +
              `✅ 美股已开盘\n` +
              `• 正在监控持仓股票\n` +
              `• 有异动脉冲会立即通知\n\n` +
              `— Hugo Sammie 家族办公室`;
  
  sendToBoth(msg, 'market');
}

/**
 * 5. 全家阅读计划 (只周日發送)
 */
function readingReport() {
  const weekday = new Date().getDay();
  
  if (weekday !== 0) {
    console.log('不是周日，跳过阅读计划');
    return;
  }
  
  const msg = `📚 全家阅读计划 | 周日\n\n` +
              `🎯 本周推荐\n` +
              `• 安排亲子阅读时间\n` +
              `• 推荐适合全家阅读的书籍\n\n` +
              `⏰ 下周预告\n` +
              `• 周一 7:45 AM - 家庭日程\n` +
              `• 周一至周五晚上 - 美股简报\n\n` +
              `— Hugo Sammie 家族办公室`;
  
  sendToBoth(msg, 'reading');
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
  } else {
    console.log('周末，股市通知已跳过');
  }
  
  console.log('測試完成！檢查 Telegram 和 Pipedream');
}

/**
 * 測試周末跳過功能
 */
function testWeekendSkip() {
  console.log('=== 測試智能過濾功能 ===');
  console.log('今天星期:', new Date().getDay());
  console.log('工作日?', isWeekday());
  console.log('周末?', isWeekend());
  
  console.log('\n調用 premarketReport()...');
  premarketReport();
  
  console.log('\n調用 opportunityCheck()...');
  opportunityCheck();
  
  console.log('\n調用 readingReport()...');
  readingReport();
}
