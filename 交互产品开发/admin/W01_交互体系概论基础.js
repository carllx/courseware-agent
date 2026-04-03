/**
 * W01 交互体系概论基础 — PPT 生成脚本
 * 使用 pptxgenjs 从零创建，遵循 Academic Minimal 设计系统
 */
const pptxgen = require("pptxgenjs");
const path = require("path");

// ═══════════════════════════════════════════════════
// 设计系统常量
// ═══════════════════════════════════════════════════
const C = {
    bg_base: "F5F0EB",
    bg_dark: "2D2926",
    bg_surface: "FFFFFF",
    bg_elevated: "EDE7E0",
    primary: "B85042",
    primary_light: "D4756A",
    secondary: "5B7B6F",
    tertiary: "C9A96E",
    text_main: "2D2926",
    text_secondary: "6B635C",
    text_muted: "A39B93",
    text_on_dark: "F5F0EB",
    border: "D6CFC7",
    divider: "E8E2DB",
};

const FONT = { title: "Georgia", body: "Calibri Light", bodyBold: "Calibri" };
const SLIDE_W = 10;    // inches
const SLIDE_H = 5.625; // inches (16:9)
const MARGIN = 0.6;

// 资产路径前缀
const ASSET_DIR = path.join(__dirname, "..", "visuals", "assets", "W01_交互体系概论基础");

// ═══════════════════════════════════════════════════
// 工厂函数（防止 pptxgenjs 对象变异）
// ═══════════════════════════════════════════════════
const cardShadow = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.08 });
const cardFill = () => ({ color: C.bg_surface });
const baseBg = () => ({ color: C.bg_base });
const darkBg = () => ({ color: C.bg_dark });

// ═══════════════════════════════════════════════════
// 主程序
// ═══════════════════════════════════════════════════
async function main() {
    const pres = new pptxgen();
    pres.layout = "LAYOUT_16x9";
    pres.author = "交互产品开发课程";
    pres.title = "W01 交互体系概论基础";

    // ───── S00: Title (封面) ─────
    {
        const s = pres.addSlide();
        s.background = darkBg();
        // 装饰条 — 顶部赤陶红细线
        s.addShape(pres.shapes.RECTANGLE, {
            x: 0, y: 0, w: SLIDE_W, h: 0.06,
            fill: { color: C.primary },
        });
        // 课程名（小字）
        s.addText("交互产品开发", {
            x: MARGIN, y: 1.4, w: SLIDE_W - MARGIN * 2, h: 0.5,
            fontSize: 16, fontFace: FONT.body, color: C.text_muted,
            align: "left",
        });
        // 主标题
        s.addText("交互体系概论基础", {
            x: MARGIN, y: 1.9, w: SLIDE_W - MARGIN * 2, h: 1.2,
            fontSize: 44, fontFace: FONT.title, color: C.text_on_dark,
            bold: true, align: "left", margin: 0,
        });
        // 副标题
        s.addText("W01 · 数字产品之殇 · 可用性与体验 · 心理模型 · 设计五原则", {
            x: MARGIN, y: 3.2, w: SLIDE_W - MARGIN * 2, h: 0.5,
            fontSize: 14, fontFace: FONT.body, color: C.primary_light,
            align: "left",
        });
        // 底部信息
        s.addText("2026 春季学期  ·  数字媒体艺术", {
            x: MARGIN, y: SLIDE_H - 0.8, w: SLIDE_W - MARGIN * 2, h: 0.4,
            fontSize: 12, fontFace: FONT.body, color: C.text_muted,
            align: "left",
        });
    }

    // ───── S01: Split — "反人类"的设计惨案 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        // 标题
        s.addText(`那些\"反人类\"的设计惨案`, {
            x: MARGIN, y: 0.4, w: 4.2, h: 0.6,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        // 左栏文字
        s.addText([
            { text: "复印机面板：上百个按键、小字说明、贴满便签贴", options: { bullet: true, breakLine: true, fontSize: 16, color: C.text_main } },
            { text: "网银转账：层层嵌套、逻辑混乱、流程绕圈", options: { bullet: true, breakLine: true, fontSize: 16, color: C.text_main } },
            { text: "", options: { breakLine: true, fontSize: 10 } },
            { text: `Alan Cooper：数字产品失败不是因为技术不够强，而是因为它们表现出了极其恶劣的\"产品行为\"。`, options: { fontSize: 14, italic: true, color: C.text_secondary } },
        ], {
            x: MARGIN, y: 1.3, w: 4.2, h: 3.5,
            fontFace: FONT.body, valign: "top",
        });
        // 右栏图片
        s.addImage({
            path: path.join(ASSET_DIR, "W01_S01.png"),
            x: 5.2, y: 0.5, w: 4.4, h: 4.6,
            sizing: { type: "contain", w: 4.4, h: 4.6 },
        });
    }

    // ───── S01b: List — 数字产品四宗罪 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("数字产品的四宗罪", {
            x: MARGIN, y: 0.4, w: 5, h: 0.6,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        const sins = [
            { num: "01", title: "粗鲁 (Rude)", desc: "把自己的错误归咎于用户" },
            { num: "02", title: "强迫人像计算机思考", desc: "要求用户按机器逻辑操作" },
            { num: "03", title: "邋遢习惯 (Sloppy)", desc: "忘记关冰箱门、转头就忘" },
            { num: "04", title: "让人类承担苦力", desc: "本该自动化的事全压给人" },
        ];
        sins.forEach((item, i) => {
            const y = 1.3 + i * 1.0;
            // 编号圆
            s.addShape(pres.shapes.OVAL, {
                x: MARGIN, y: y + 0.05, w: 0.45, h: 0.45,
                fill: { color: C.primary },
            });
            s.addText(item.num, {
                x: MARGIN, y: y + 0.05, w: 0.45, h: 0.45,
                fontSize: 14, fontFace: FONT.bodyBold, color: C.text_on_dark,
                align: "center", valign: "middle", margin: 0,
            });
            // 标题
            s.addText(item.title, {
                x: MARGIN + 0.6, y: y, w: 3.5, h: 0.35,
                fontSize: 18, fontFace: FONT.bodyBold, color: C.text_main, bold: true, margin: 0,
            });
            // 描述
            s.addText(item.desc, {
                x: MARGIN + 0.6, y: y + 0.35, w: 3.5, h: 0.3,
                fontSize: 14, fontFace: FONT.body, color: C.text_secondary, margin: 0,
            });
        });
        // 右侧 Asset
        s.addImage({
            path: path.join(ASSET_DIR, "W01_S01b.png"),
            x: 5.2, y: 0.8, w: 4.4, h: 4.2,
            sizing: { type: "contain", w: 4.4, h: 4.2 },
        });
    }

    // ───── S01c: List — 数字化排斥 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("数字化的代价：谁被抛在了身后？", {
            x: MARGIN, y: 0.4, w: 5, h: 0.6,
            fontSize: 26, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        const groups = [
            "不使用智能手机的老年人",
            "手机没电或没有移动数据的人",
            "不愿提供个人信息的隐私敏感用户",
            "使用辅助技术的残障人士",
        ];
        s.addText(groups.map((g, i) => ({
            text: g,
            options: { bullet: true, breakLine: i < groups.length - 1, fontSize: 16, color: C.text_main },
        })), {
            x: MARGIN, y: 1.3, w: 4.2, h: 3.0,
            fontFace: FONT.body, valign: "top", paraSpaceAfter: 10,
        });
        s.addText("数字化本身就可能成为痛点的来源。", {
            x: MARGIN, y: 4.0, w: 4.2, h: 0.4,
            fontSize: 14, fontFace: FONT.body, italic: true, color: C.primary, margin: 0,
        });
        s.addImage({
            path: path.join(ASSET_DIR, "W01_S01c.png"),
            x: 5.2, y: 0.5, w: 4.4, h: 4.6,
            sizing: { type: "contain", w: 4.4, h: 4.6 },
        });
    }

    // ───── S02: Split — 什么是交互设计？ ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("什么是交互设计？", {
            x: MARGIN, y: 0.4, w: 5, h: 0.6,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        s.addText([
            { text: "Yvonne Rogers 经典定义：", options: { breakLine: true, fontSize: 14, color: C.text_muted, bold: true } },
            { text: "", options: { breakLine: true, fontSize: 8 } },
            { text: "\"设计支持人们日常工作和生活的交互产品\"", options: { breakLine: true, fontSize: 20, italic: true, color: C.primary, bold: true } },
            { text: "", options: { breakLine: true, fontSize: 12 } },
            { text: "关注产品的行为方式，而非外观。", options: { breakLine: true, fontSize: 16, color: C.text_main } },
            { text: "我们不仅在设计屏幕，更在设计人类的行为模式和情绪流。", options: { fontSize: 16, color: C.text_main } },
        ], {
            x: MARGIN, y: 1.2, w: 4.2, h: 3.5,
            fontFace: FONT.body, valign: "top",
        });
        s.addImage({
            path: path.join(ASSET_DIR, "W01_S02.png"),
            x: 5.2, y: 0.5, w: 4.4, h: 4.6,
            sizing: { type: "contain", w: 4.4, h: 4.6 },
        });
    }

    // ───── S02a: Split — 可用性六大目标 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("可用性的六大目标", {
            x: MARGIN, y: 0.4, w: 5, h: 0.6,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        const goals = [
            { en: "Effectiveness", cn: "有效性", desc: "能让用户完成想做的事" },
            { en: "Efficiency", cn: "效率", desc: "完成任务的速度如何" },
            { en: "Safety", cn: "安全性", desc: "防止犯错 & 从错误中恢复" },
            { en: "Utility", cn: "效用性", desc: "功能集是否恰当" },
            { en: "Learnability", cn: "可学习性", desc: "新手上手有多快" },
            { en: "Memorability", cn: "易记性", desc: "久别重逢是否仍然记得" },
        ];
        goals.forEach((g, i) => {
            const y = 1.2 + i * 0.65;
            // 序号
            s.addText(`${i + 1}`, {
                x: MARGIN, y, w: 0.3, h: 0.35,
                fontSize: 16, fontFace: FONT.bodyBold, color: C.primary, bold: true, margin: 0,
            });
            // 中文名
            s.addText(g.cn, {
                x: MARGIN + 0.35, y, w: 1.2, h: 0.35,
                fontSize: 16, fontFace: FONT.bodyBold, color: C.text_main, bold: true, margin: 0,
            });
            // 描述
            s.addText(g.desc, {
                x: MARGIN + 1.6, y, w: 2.6, h: 0.35,
                fontSize: 13, fontFace: FONT.body, color: C.text_secondary, margin: 0,
            });
        });
        s.addImage({
            path: path.join(ASSET_DIR, "W01_S02a.png"),
            x: 5.2, y: 0.5, w: 4.4, h: 4.6,
            sizing: { type: "contain", w: 4.4, h: 4.6 },
        });
    }

    // ───── S02b: Comparison — 体验目标正反面 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("用户体验目标：硬币的两面", {
            x: MARGIN, y: 0.35, w: SLIDE_W - MARGIN * 2, h: 0.55,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        // 左列 - 正面 (苔藓绿)
        const colW = 4.0;
        const colGap = 0.4;
        const lx = MARGIN;
        const rx = MARGIN + colW + colGap;
        // 左标签
        s.addShape(pres.shapes.RECTANGLE, {
            x: lx, y: 1.1, w: colW, h: 0.4,
            fill: { color: C.secondary },
        });
        s.addText("✓  正面体验 (Desirable)", {
            x: lx, y: 1.1, w: colW, h: 0.4,
            fontSize: 14, fontFace: FONT.bodyBold, color: C.text_on_dark, bold: true,
            align: "center", valign: "middle", margin: 0,
        });
        const positives = ["令人愉悦的", "有启发性的", "美学平衡的", "令人沉浸的", "支持创造力"];
        s.addText(positives.map((p, i) => ({
            text: p, options: { bullet: true, breakLine: i < positives.length - 1, fontSize: 16, color: C.text_main },
        })), {
            x: lx + 0.2, y: 1.7, w: colW - 0.4, h: 3.2,
            fontFace: FONT.body, valign: "top", paraSpaceAfter: 8,
        });
        // 右标签
        s.addShape(pres.shapes.RECTANGLE, {
            x: rx, y: 1.1, w: colW, h: 0.4,
            fill: { color: C.primary },
        });
        s.addText("✗  反面体验 (Undesirable)", {
            x: rx, y: 1.1, w: colW, h: 0.4,
            fontSize: 14, fontFace: FONT.bodyBold, color: C.text_on_dark, bold: true,
            align: "center", valign: "middle", margin: 0,
        });
        const negatives = ["令人挫败的", "让人感到被愚弄", "高高在上的", "令人毛骨悚然的", "具有欺骗性的"];
        s.addText(negatives.map((n, i) => ({
            text: n, options: { bullet: true, breakLine: i < negatives.length - 1, fontSize: 16, color: C.text_main },
        })), {
            x: rx + 0.2, y: 1.7, w: colW - 0.4, h: 3.2,
            fontFace: FONT.body, valign: "top", paraSpaceAfter: 8,
        });
        // 底部提示
        s.addText("好的评估必须同时触及正反两面。", {
            x: MARGIN, y: SLIDE_H - 0.65, w: SLIDE_W - MARGIN * 2, h: 0.35,
            fontSize: 13, fontFace: FONT.body, italic: true, color: C.text_muted, align: "center",
        });
    }

    // ───── S03: Split — 三大模型 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("三大模型：代沟的根源", {
            x: MARGIN, y: 0.4, w: 5, h: 0.6,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        const models = [
            { title: "工程实施模型", en: "Implementation Model", desc: "代码怎么写、数据怎么存", accent: C.text_muted },
            { title: "表现模型", en: "Represented Model", desc: "设计师创造的界面形式", accent: C.tertiary },
            { title: "用户心理模型", en: "Mental Model", desc: "用户脑中的预期与信念", accent: C.primary },
        ];
        models.forEach((m, i) => {
            const y = 1.2 + i * 1.2;
            // 左侧色块标记
            s.addShape(pres.shapes.RECTANGLE, {
                x: MARGIN, y, w: 0.08, h: 0.9,
                fill: { color: m.accent },
            });
            s.addText(m.title, {
                x: MARGIN + 0.2, y, w: 3.8, h: 0.4,
                fontSize: 18, fontFace: FONT.bodyBold, color: C.text_main, bold: true, margin: 0,
            });
            s.addText(`${m.en} — ${m.desc}`, {
                x: MARGIN + 0.2, y: y + 0.4, w: 3.8, h: 0.35,
                fontSize: 13, fontFace: FONT.body, color: C.text_secondary, margin: 0,
            });
        });
        // 底部要点
        s.addText("成功的交互 = 表现模型与用户心理模型完全一致", {
            x: MARGIN, y: 4.6, w: 4.5, h: 0.4,
            fontSize: 14, fontFace: FONT.body, italic: true, color: C.primary, margin: 0,
        });
        s.addImage({
            path: path.join(ASSET_DIR, "W01_S03.png"),
            x: 5.2, y: 0.5, w: 4.4, h: 4.6,
            sizing: { type: "contain", w: 4.4, h: 4.6 },
        });
    }

    // ───── S04: Split — 目标 ≠ 任务 ≠ 活动 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("目标 ≠ 活动 ≠ 任务", {
            x: MARGIN, y: 0.4, w: 5, h: 0.6,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        const layers = [
            { label: "目标 Goals", note: "为什么？不随技术变化", color: C.primary },
            { label: "活动 Activities", note: "做什么大事？", color: C.tertiary },
            { label: "任务 Tasks", note: "具体步骤？随技术变化", color: C.text_muted },
        ];
        layers.forEach((l, i) => {
            const y = 1.2 + i * 1.2;
            s.addShape(pres.shapes.RECTANGLE, {
                x: MARGIN, y, w: 4.2, h: 0.9,
                fill: { color: C.bg_surface },
                shadow: cardShadow(),
            });
            s.addShape(pres.shapes.RECTANGLE, {
                x: MARGIN, y, w: 0.08, h: 0.9,
                fill: { color: l.color },
            });
            s.addText(l.label, {
                x: MARGIN + 0.2, y, w: 3.8, h: 0.45,
                fontSize: 18, fontFace: FONT.bodyBold, color: C.text_main, bold: true, margin: 0, valign: "bottom",
            });
            s.addText(l.note, {
                x: MARGIN + 0.2, y: y + 0.45, w: 3.8, h: 0.35,
                fontSize: 13, fontFace: FONT.body, color: C.text_secondary, margin: 0,
            });
        });
        s.addImage({
            path: path.join(ASSET_DIR, "W01_S04.png"),
            x: 5.2, y: 0.5, w: 4.4, h: 4.6,
            sizing: { type: "contain", w: 4.4, h: 4.6 },
        });
    }

    // ───── S05: Grid — 暗黑模式 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("暗黑模式：设计师的职业底线", {
            x: MARGIN, y: 0.35, w: SLIDE_W - MARGIN * 2, h: 0.55,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        const cards = [
            { title: "偷加购物车", en: "Sneak into Basket", desc: "默认勾选保险、加急配送、VIP…" },
            { title: "退订地狱", en: "Roach Motel", desc: "注册一键，退订五步迷宫" },
            { title: "虚假紧迫感", en: "False Urgency", desc: `\"仅剩 2 间房！\" — 数字可能是编造的` },
        ];
        const cardW = 2.7;
        const gap = 0.35;
        const startX = (SLIDE_W - (cardW * 3 + gap * 2)) / 2;
        cards.forEach((c, i) => {
            const cx = startX + i * (cardW + gap);
            s.addShape(pres.shapes.RECTANGLE, {
                x: cx, y: 1.1, w: cardW, h: 3.6,
                fill: cardFill(), shadow: cardShadow(),
            });
            // 顶部色条
            s.addShape(pres.shapes.RECTANGLE, {
                x: cx, y: 1.1, w: cardW, h: 0.06,
                fill: { color: C.primary },
            });
            s.addText(c.title, {
                x: cx + 0.15, y: 1.35, w: cardW - 0.3, h: 0.4,
                fontSize: 18, fontFace: FONT.bodyBold, color: C.text_main, bold: true, margin: 0,
            });
            s.addText(c.en, {
                x: cx + 0.15, y: 1.75, w: cardW - 0.3, h: 0.3,
                fontSize: 11, fontFace: FONT.body, color: C.text_muted, margin: 0,
            });
            s.addText(c.desc, {
                x: cx + 0.15, y: 2.2, w: cardW - 0.3, h: 2.3,
                fontSize: 14, fontFace: FONT.body, color: C.text_secondary, valign: "top", margin: 0,
            });
        });
        // 底栏警示
        s.addText("⚠ 用约束来保护用户，而不是用约束来剥削用户。", {
            x: MARGIN, y: SLIDE_H - 0.6, w: SLIDE_W - MARGIN * 2, h: 0.35,
            fontSize: 14, fontFace: FONT.body, italic: true, color: C.primary, align: "center",
        });
    }

    // ───── S06: Split — 示能与示能信号 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("示能 (Affordance) 与示能信号 (Signifier)", {
            x: MARGIN, y: 0.4, w: 5, h: 0.6,
            fontSize: 24, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        s.addText([
            { text: "物理示能", options: { bold: true, breakLine: true, fontSize: 18, color: C.primary } },
            { text: "物体的物理属性 → 操作可能性", options: { breakLine: true, fontSize: 14, color: C.text_secondary } },
            { text: `例：平推板暗示\"推\"，把手暗示\"拉\"`, options: { breakLine: true, fontSize: 14, color: C.text_secondary } },
            { text: "", options: { breakLine: true, fontSize: 10 } },
            { text: "示能信号 (数字)", options: { bold: true, breakLine: true, fontSize: 18, color: C.secondary } },
            { text: `视觉信号\"暗示\"可交互`, options: { breakLine: true, fontSize: 14, color: C.text_secondary } },
            { text: "例：阴影按钮、下划线蓝字", options: { breakLine: true, fontSize: 14, color: C.text_secondary } },
            { text: "", options: { breakLine: true, fontSize: 10 } },
            { text: "诺曼澄清：数字屏幕上几乎不存在真正的物理示能。", options: { fontSize: 14, italic: true, color: C.text_muted } },
        ], {
            x: MARGIN, y: 1.2, w: 4.3, h: 3.8,
            fontFace: FONT.body, valign: "top",
        });
        s.addImage({
            path: path.join(ASSET_DIR, "W01_S06.png"),
            x: 5.2, y: 0.5, w: 4.4, h: 4.6,
            sizing: { type: "contain", w: 4.4, h: 4.6 },
        });
    }

    // ───── S07: Image — 多模态反馈 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("多模态反馈：软硬结合", {
            x: MARGIN, y: 0.4, w: SLIDE_W - MARGIN * 2, h: 0.5,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        // 大图居中
        s.addImage({
            path: path.join(ASSET_DIR, "W01_S07.png"),
            x: 1.0, y: 1.1, w: 8.0, h: 3.8,
            sizing: { type: "contain", w: 8.0, h: 3.8 },
        });
        s.addText("Nest 恒温器 · AirPods 入耳检测 — 跨越软硬边界的自然操作邀请", {
            x: MARGIN, y: SLIDE_H - 0.6, w: SLIDE_W - MARGIN * 2, h: 0.35,
            fontSize: 13, fontFace: FONT.body, italic: true, color: C.text_muted, align: "center",
        });
    }

    // ───── S08: Grid — 无障碍设计 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("无障碍与包容性设计", {
            x: MARGIN, y: 0.35, w: SLIDE_W - MARGIN * 2, h: 0.55,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        const types = [
            { title: "永久性", desc: "长期轮椅使用者\n失明者使用屏幕阅读器", accent: C.primary },
            { title: "临时性", desc: "手术恢复期\n手臂骨折单手操作", accent: C.tertiary },
            { title: "情境性", desc: "嘈杂地铁中听不清\n强光下看不清屏幕", accent: C.secondary },
        ];
        const tw = 2.7;
        const tgap = 0.35;
        const tsx = (SLIDE_W - (tw * 3 + tgap * 2)) / 2;
        types.forEach((t, i) => {
            const tx = tsx + i * (tw + tgap);
            s.addShape(pres.shapes.RECTANGLE, {
                x: tx, y: 1.1, w: tw, h: 3.4,
                fill: cardFill(), shadow: cardShadow(),
            });
            s.addShape(pres.shapes.RECTANGLE, {
                x: tx, y: 1.1, w: tw, h: 0.06,
                fill: { color: t.accent },
            });
            s.addText(t.title, {
                x: tx + 0.15, y: 1.35, w: tw - 0.3, h: 0.4,
                fontSize: 20, fontFace: FONT.bodyBold, color: C.text_main, bold: true, margin: 0,
            });
            s.addText(t.desc, {
                x: tx + 0.15, y: 1.95, w: tw - 0.3, h: 2.3,
                fontSize: 14, fontFace: FONT.body, color: C.text_secondary, valign: "top", margin: 0,
            });
        });
        s.addText(`每个人在一生中都会经历\"情境性残障\"。为最困难的用户设计，催生普世创新。`, {
            x: MARGIN, y: SLIDE_H - 0.6, w: SLIDE_W - MARGIN * 2, h: 0.35,
            fontSize: 13, fontFace: FONT.body, italic: true, color: C.text_muted, align: "center",
        });
    }

    // ───── S09: Split — Exp1 敏捷洞察 ─────
    {
        const s = pres.addSlide();
        s.background = baseBg();
        s.addText("Exp1：敏捷洞察与 MVP", {
            x: MARGIN, y: 0.4, w: 5, h: 0.6,
            fontSize: 28, fontFace: FONT.title, color: C.text_main, bold: true, margin: 0,
        });
        s.addText([
            { text: "Think → Make → Check 循环", options: { bold: true, breakLine: true, fontSize: 18, color: C.primary } },
            { text: "", options: { breakLine: true, fontSize: 8 } },
            { text: "阶段 1: 定性研究", options: { bold: true, breakLine: true, fontSize: 16, color: C.text_main } },
            { text: "寻找真问题、访谈非自身熟悉群体", options: { breakLine: true, fontSize: 14, color: C.text_secondary } },
            { text: "", options: { breakLine: true, fontSize: 6 } },
            { text: "阶段 2: 最小可行性产品 (MVP)", options: { bold: true, breakLine: true, fontSize: 16, color: C.text_main } },
            { text: "只留核心痛点的那一条业务主线", options: { breakLine: true, fontSize: 14, color: C.text_secondary } },
            { text: "", options: { breakLine: true, fontSize: 6 } },
            { text: "阶段 3: 状态流转白板图", options: { bold: true, breakLine: true, fontSize: 16, color: C.text_main } },
            { text: "线框草图 + 流程白板", options: { fontSize: 14, color: C.text_secondary } },
        ], {
            x: MARGIN, y: 1.15, w: 4.3, h: 3.8,
            fontFace: FONT.body, valign: "top",
        });
        s.addImage({
            path: path.join(ASSET_DIR, "W01_S09.png"),
            x: 5.2, y: 0.5, w: 4.4, h: 4.6,
            sizing: { type: "contain", w: 4.4, h: 4.6 },
        });
    }

    // ───── S10: CTA (收尾页) ─────
    {
        const s = pres.addSlide();
        s.background = darkBg();
        // 顶部赤陶色条
        s.addShape(pres.shapes.RECTANGLE, {
            x: 0, y: 0, w: SLIDE_W, h: 0.06,
            fill: { color: C.primary },
        });
        s.addText("课堂总结", {
            x: MARGIN, y: 0.6, w: SLIDE_W - MARGIN * 2, h: 0.7,
            fontSize: 36, fontFace: FONT.title, color: C.text_on_dark, bold: true, margin: 0,
        });
        const summaryItems = [
            `数字产品\"四宗罪\" → 认知摩擦的根源`,
            "可用性目标（理性底线）+ 体验目标（感性上限）",
            "心理模型 · 工程模型 · 表现模型 — 三角关系",
            "五大设计原则：可见性 · 反馈 · 约束 · 一致性 · 示能",
            "Exp1 启动：寻找痛点 → 定性访谈 → MVP → 白板图",
        ];
        s.addText(summaryItems.map((item, i) => ({
            text: item,
            options: { bullet: true, breakLine: i < summaryItems.length - 1, fontSize: 16, color: C.text_on_dark },
        })), {
            x: MARGIN, y: 1.5, w: SLIDE_W - MARGIN * 2, h: 2.8,
            fontFace: FONT.body, valign: "top", paraSpaceAfter: 8,
        });
        // 课后任务
        s.addShape(pres.shapes.RECTANGLE, {
            x: MARGIN, y: 4.3, w: SLIDE_W - MARGIN * 2, h: 0.04,
            fill: { color: C.primary, transparency: 50 },
        });
        s.addText("课后任务：选一款高频 App，逆向拆解可用性（6维打分）+ 体验目标（正反面），800 字报告", {
            x: MARGIN, y: 4.5, w: SLIDE_W - MARGIN * 2, h: 0.5,
            fontSize: 14, fontFace: FONT.body, color: C.primary_light, margin: 0,
        });
    }

    // ═══════════════════════════════════════════════════
    // 输出
    // ═══════════════════════════════════════════════════
    const outPath = path.join(__dirname, "W01_交互体系概论基础.pptx");
    await pres.writeFile({ fileName: outPath });
    console.log(`✅ PPT 已生成: ${outPath}`);
}

main().catch(err => { console.error("❌ 生成失败:", err); process.exit(1); });
