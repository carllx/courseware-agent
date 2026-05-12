import { useState, useMemo, useEffect } from "react";
import { useProgress } from "../contexts/ProgressContext";
import { useValidation } from "../contexts/ValidationContext";
import "../styles/outline-sidebar.css";

/**
 * OutlineSidebar — 左侧结构化章节目录地图
 *
 * 替代 ModuleRail + SectionPills + HealthDot + scroll-spy-track。
 * 提供全局 "You-Are-Here" 定位感与进度反馈。
 *
 * 策略：
 *   - 当前模块(H2)：完全展开 H3 子节
 *   - 相邻模块(±1)：仅显示 H2 标题
 *   - 其余模块：折叠但可见（单行 H2）
 *   - 底部：健康摘要（从 HealthDot 吸纳的 manifest 统计）
 */
export default function OutlineSidebar({
  manifest,
  currentSectionIdx,
  activeParagraphIdx,
  onSwitchSection,
  onNavigateToParagraph,
  courseId,
  scriptName,
  mobileDrawerOpen,
  onCloseMobileDrawer,
}) {
  const [collapsed, setCollapsed] = useState(false);
  const [validationOpen, setValidationOpen] = useState(false);
  const progress = useProgress();
  const { validation, gateLevel } = useValidation();

  // 保证在移动端 (<=900px) 绝不进入桌面版的折叠 DOM 模式
  // 否则 Drawer 就算划出来也只有 48px
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth <= 900 && collapsed) {
        setCollapsed(false);
      }
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [collapsed]);

  if (!manifest) return null;

  const sections = manifest.sections || [];
  const modules = manifest.modules || [];

  // 折叠态：仅显示窄条
  if (collapsed) {
    return (
      <div className="outline-sidebar outline-sidebar--collapsed">
        <button
          className="outline-sidebar-toggle"
          onClick={() => setCollapsed(false)}
          title="展开目录"
        >
          <span className="toggle-icon">☰</span>
        </button>
        {/* 微型进度指示 */}
        <div className="outline-mini-progress">
          {sections.map((_, idx) => (
            <div
              key={idx}
              className={`mini-dot ${idx === currentSectionIdx ? "active" : ""}`}
            />
          ))}
        </div>
      </div>
    );
  }

  return (
    <>
      {/* 移动端全屏透明遮罩 (Backdrop) */}
      <div 
        className={`outline-sidebar-overlay ${mobileDrawerOpen ? 'active' : ''}`}
        onClick={onCloseMobileDrawer}
        aria-hidden="true"
      />

      <aside className={`outline-sidebar ${mobileDrawerOpen ? 'mobile-drawer-open' : ''}`}>
        {/* 头部：课程名 + 折叠按钮 */}
        <div className="outline-header">
        <span className="outline-course-name" title={manifest.course}>
          {manifest.script}
        </span>
        <button
          className="outline-sidebar-toggle"
          onClick={() => setCollapsed(true)}
          title="收起目录"
        >
          ✕
        </button>
      </div>

      {/* ARC-02/03: 全局水位分析条 - 双轨分离制 (含视频时长归因) */}
      {manifest.stats && (() => {
        const { 
          budgetMinutes = 90, 
          theoryBudgetMinutes = 90, 
          practiceBudgetMinutes = 0,
          lectureMinutes = 0, 
          activityMinutes = 0,
          mediaLectureMinutes = 0,
          mediaActivityMinutes = 0,
          speechRate = 180,
        } = manifest.stats;
        
        // ARC-03: 视频时长归入对应时间池
        const effectiveLecture = lectureMinutes + mediaLectureMinutes;
        const effectiveActivity = activityMinutes + mediaActivityMinutes;
        const totalMedia = mediaLectureMinutes + mediaActivityMinutes;

        // P1: 修正命名——toClassHours 转换为"学时"(45分钟/学时)，而非"小时"
        const toClassHours = (m) => (m / 45).toFixed(1);
        const lH = Number(toClassHours(effectiveLecture));
        const aH = Number(toClassHours(effectiveActivity));
        // P1: 统一精度为 .toFixed(1)，消除展示值与检测阈值的认知不一致
        const tBh = toClassHours(theoryBudgetMinutes);
        const pBh = toClassHours(practiceBudgetMinutes);

        // 理论讲授 Track 计算
        const lMax = Math.max(theoryBudgetMinutes, effectiveLecture, 1); 
        const lFillP = (effectiveLecture / lMax) * 100;
        const lThresholdP = (theoryBudgetMinutes / lMax) * 100;
        const lOvertime = effectiveLecture > theoryBudgetMinutes;

        // 实践活动 Track 计算
        const pMax = Math.max(practiceBudgetMinutes, effectiveActivity, 1); 
        const pFillP = (effectiveActivity / pMax) * 100;
        const pThresholdP = (practiceBudgetMinutes / pMax) * 100;
        // P2: 零预算场景——当计划外活动 ≥ 5 分钟时判定为超载
        // 避免微型课堂互动（如30秒举手投票）误触发警告
        const pOvertime = practiceBudgetMinutes > 0
          ? effectiveActivity > practiceBudgetMinutes
          : effectiveActivity >= 5;

        let ratioText = '纯讲授';
        if (effectiveActivity > 0) {
          const ratio = (effectiveLecture / effectiveActivity).toFixed(1);
          ratioText = `讲练比 ${ratio}:1`;
        } else if (effectiveLecture === 0) {
          ratioText = '无内容';
        }

        // ARC-03: 视频时长信息
        const mediaLecTag = mediaLectureMinutes > 0 ? ` (含📹${toClassHours(mediaLectureMinutes)})` : '';
        const mediaActTag = mediaActivityMinutes > 0 ? ` (含📹${toClassHours(mediaActivityMinutes)})` : '';
        // 语速提示信息
        const rateInfo = speechRate !== 180 ? ` | 语速 ${speechRate}字/分` : '';


        return (
          <div className="outline-pacing-container">
            <div className="pacing-global-header">
              <span className="pacing-title">课程进度剖析</span>
              <span className="pacing-ratio">{ratioText}{totalMedia > 0 && <span className="pacing-media-badge" title={`视频素材合计 ${toClassHours(totalMedia)} 学时`}>📹</span>}</span>
            </div>

            {/* Track 1: 理论讲授 */}
            <div className="pacing-track-container" title={`理论包含讲授与互动，系统预估字数换算${mediaLecTag}${rateInfo}\n实际：${lH.toFixed(1)} 学时 | 预设：${tBh} 学时`}>
              <div className="pacing-track-header">
                <span className={`pacing-track-label ${lOvertime ? 'overtime-warn' : ''}`}>讲授 ({lH.toFixed(1)}/{tBh} 学)</span>
              </div>
              <div className="pacing-stacked-bar">
                {lFillP > 0 && <div className="pacing-fill lecture" style={{width: `${lFillP}%`}} />}
                {lOvertime && (
                  <div className="pacing-overtime-overlay" style={{ left: `${lThresholdP}%`, right: 0 }} title="讲授超时超载" />
                )}
              </div>
            </div>

            {/* Track 2: 实践活动 (仅当存在预设或实际时显示) */}
            {(practiceBudgetMinutes > 0 || effectiveActivity > 0) && (
              <div className="pacing-track-container" title={`由 [ACTIVITY] 标签 + 视频案例驱动${mediaActTag}\n实际：${aH.toFixed(1)} 学时 | 预设：${pBh} 学时`}>
                <div className="pacing-track-header">
                  <span className={`pacing-track-label ${pOvertime ? 'overtime-warn' : ''}`}>实践 ({aH.toFixed(1)}/{pBh} 学)</span>
                </div>
                <div className="pacing-stacked-bar">
                  {pFillP > 0 && <div className="pacing-fill activity" style={{width: `${pFillP}%`}} />}
                  {pOvertime && (
                    <div className="pacing-overtime-overlay" style={{ left: `${Math.max(0.1, pThresholdP)}%`, right: 0 }} title="实践时数超载" />
                  )}
                </div>
              </div>
            )}
          </div>
        );
      })()}

      {/* 目录树 */}
      <nav className="outline-tree">
        {sections.map((sec, idx) => {
          const mod = modules[idx];
          const isActive = idx === currentSectionIdx;
          const isRead = progress?.isRead?.(courseId, scriptName, sec.id);
          const subSections = sec.subSections || [];
          const hasSubSections = subSections.length > 0;

          // 色相强调
          const hue = mod?.colorHue ?? 210;
          const accentColor = `hsl(${hue}, 60%, 55%)`;

          // 当前激活子节推断
          // ARC-01 v2: 基于 paragraph 锚点判断激活子节
          let activeSubIdx = -1;
          if (isActive && hasSubSections) {
            const effectiveParaIdx = activeParagraphIdx >= 0 ? activeParagraphIdx : 0;
            for (let i = 0; i < subSections.length; i++) {
              if (subSections[i].startParagraph <= effectiveParaIdx) {
                activeSubIdx = i;
              }
            }
          }

          return (
            <div
              key={sec.id}
              className={`outline-module ${isActive ? "active" : ""}`}
            >
              {/* H2 模块标题行 */}
              <button
                className={`outline-module-btn ${isActive ? "active" : ""} ${isRead && !isActive ? "read" : ""}`}
                style={{ "--module-accent": accentColor }}
                onClick={() => onSwitchSection(idx)}
                title={mod?.transitionHint || sec.title}
              >
                <span className="outline-module-accent" />
                <span className="outline-module-icon">
                  {mod?.heroIcon || "📖"}
                </span>
                <span className="outline-module-label">
                  {_shortTitle(sec.title)}
                </span>
                {isRead && !isActive && (
                  <span className="outline-check">✓</span>
                )}
              </button>

              {/* H3 子节列表：仅当前模块展开 */}
              {isActive && hasSubSections && (
                <div className="outline-subsections">
                  {subSections.map((sub, subIdx) => {
                    const isSubActive = subIdx === activeSubIdx;
                    return (
                      <button
                        key={sub.id}
                        className={`outline-sub-btn ${isSubActive ? "active" : ""}`}
                        onClick={() => onNavigateToParagraph(sub.startParagraph)}
                        title={sub.title}
                      >
                        <span className="outline-sub-indicator" />
                        <span className="outline-sub-label">{sub.title}</span>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </nav>

    </aside>
  </>
  );
}

/**
 * 缩短模块标题
 */
function _shortTitle(title) {
  let s = title.replace(/^Module\s*\d+\s*[:：]\s*/i, "");
  s = s.replace(/\s*\(\d+\s*分钟\)\s*$/, "");
  s = s.replace(/\*\*/g, "");
  if (s.length > 20) s = s.slice(0, 20) + "…";
  return s;
}
