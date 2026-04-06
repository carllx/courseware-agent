import { useState, useMemo } from "react";
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
  currentSlideIdx,
  onSwitchSection,
  onSwitchSlide,
  courseId,
  scriptName,
}) {
  const [collapsed, setCollapsed] = useState(false);
  const [validationOpen, setValidationOpen] = useState(false);
  const progress = useProgress();
  const { validation, gateLevel } = useValidation();

  // 健康统计（从 HealthDot 吸纳）
  const healthStats = useMemo(() => {
    if (!manifest?.sections) return null;
    let totalSlides = 0;
    let brokenSlides = 0;
    let underfilledModules = 0;
    let emptyModules = 0;

    manifest.sections.forEach((sec) => {
      if (!sec.paragraphs || sec.paragraphs.length === 0) emptyModules++;
      if (sec.fillRatio != null && sec.fillRatio < 0.8) underfilledModules++;
      if (sec.slides) {
        sec.slides.forEach((slide) => {
          totalSlides++;
          if (slide.assetExpected && !slide.image) brokenSlides++;
        });
      }
    });

    let color = "green";
    if (emptyModules > 0 || underfilledModules > 0) color = "red";
    else if (brokenSlides > 0) color = "yellow";
  }, [manifest]);

  // 从 HMR ValidationContext 获取动态验证详情
  const validationStats = useMemo(() => {
    if (!validation) return null;
    const { validators } = validation;
    const lengthData = validators?.length;
    const visualsData = validators?.visuals;

    if (!lengthData) return null;
    const modules = lengthData.modules || [];
    const underfilledCount = modules.filter(
      (m) => m.fillRatio != null && m.fillRatio < 0.8,
    ).length;
    const draftCount = modules.filter((m) => m.isDraft).length;
    const tagDeficitCount = modules.filter((m) => m.tagDeficit > 0).length;
    const missingVisuals = visualsData?.summary?.missing || 0;

    return {
      underfilledCount,
      draftCount,
      tagDeficitCount,
      missingVisuals,
      modules,
      lengthData,
      visualsData,
    };
  }, [validation]);

  // 优先级：HMR 动态数据 > manifest 静态数据
  const displayStats = useMemo(() => {
    let text = `${healthStats?.totalSlides || 0} slides`;
    let color = healthStats?.color || "green";
    let issues = 0;
    let issueTexts = [];

    if (validationStats) {
      issues =
        validationStats.underfilledCount +
        validationStats.draftCount +
        validationStats.missingVisuals;
      if (validationStats.missingVisuals > 0)
        issueTexts.push(`${validationStats.missingVisuals} 断链`);
      if (validationStats.underfilledCount > 0)
        issueTexts.push(`${validationStats.underfilledCount} 不足`);
      if (validationStats.tagDeficitCount > 0)
        issueTexts.push(`${validationStats.tagDeficitCount} 缺签`);
      if (issues > 0)
        color = validationStats.missingVisuals > 0 ? "yellow" : "red";
      else color = "green";
    } else if (healthStats) {
      if (healthStats.brokenSlides > 0)
        issueTexts.push(`${healthStats.brokenSlides} 断链`);
      if (healthStats.underfilledModules > 0)
        issueTexts.push(`${healthStats.underfilledModules} 不足`);
    }

    if (issueTexts.length > 0) {
      text += ` · ${issueTexts.join(" ")}`;
    } else {
      text += ` · 健康`;
    }

    return { text, color, hasValidation: !!validationStats };
  }, [healthStats, validationStats]);

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
    <aside className="outline-sidebar">
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
          let activeSubIdx = -1;
          if (isActive && hasSubSections) {
            for (let i = 0; i < subSections.length; i++) {
              if (subSections[i].startSlide <= currentSlideIdx) {
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
                        onClick={() => onSwitchSlide(sub.startSlide)}
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

      {/* 底部健康摘要 */}
      <div className="outline-health-container">
        <button
          className="outline-health clickable"
          onClick={() => setValidationOpen(!validationOpen)}
          title="查看验证详情"
        >
          <div className="outline-health-info">
            <span className="outline-health-dot" />
            <span className="outline-health-text">{displayStats.text}</span>
          </div>
          <span className="outline-health-action">🔍 验证</span>
        </button>

        {/* 弹出验证详情面板 */}
        {validationOpen && (
          <div className="outline-validation-popover">
            <div className="validation-panel-header">
              <span>🔍 验证详情</span>
              <button
                className="validation-close"
                onClick={() => setValidationOpen(false)}
              >
                ×
              </button>
            </div>

            {!validationStats ? (
              <div className="validation-section">
                <div className="validation-hint">
                  ⏳ 等待编辑器保存触发实时验证...
                </div>
              </div>
            ) : (
              <>
                {gateLevel >= 2 && (
                  <div className="validation-gate-warning">
                    ⚠️ 字数严重不足，视觉检查已折弱
                  </div>
                )}

                {validationStats.lengthData && (
                  <div className="validation-section">
                    <div className="validation-section-title">📝 字数验证</div>
                    {validationStats.modules.map((mod, i) => {
                      if (mod.fillRatio == null) return null;
                      const percent = Math.round(mod.fillRatio * 100);
                      const status =
                        mod.fillRatio >= 1.0
                          ? "ok"
                          : mod.fillRatio >= 0.8
                            ? "warn"
                            : "fail";
                      return (
                        <div
                          key={i}
                          className={`validation-module-row ${status}`}
                        >
                          <span
                            className="validation-module-name"
                            title={mod.module}
                          >
                            {mod.module.length > 18
                              ? mod.module.slice(0, 16) + ".."
                              : mod.module}
                          </span>
                          <div className="validation-mini-bar">
                            <div
                              className={`validation-mini-fill ${status}`}
                              style={{ width: `${Math.min(percent, 100)}%` }}
                            />
                          </div>
                          <span className={`validation-percent ${status}`}>
                            {percent}%
                          </span>
                        </div>
                      );
                    })}
                    {validationStats.tagDeficitCount > 0 && (
                      <div className="validation-hint">
                        🏷️ {validationStats.tagDeficitCount} 个模块标签密度不足
                      </div>
                    )}
                  </div>
                )}

                {validationStats.visualsData && gateLevel < 2 && (
                  <div className="validation-section">
                    <div className="validation-section-title">🔗 视觉素材</div>
                    {validationStats.visualsData.missing?.length > 0 ? (
                      validationStats.visualsData.missing.map((m, i) => (
                        <div key={i} className="validation-missing-row">
                          <span className="validation-slide-id">
                            {m.slideId}
                          </span>
                          <button
                            className="validation-jump"
                            onClick={() => {
                              if (m.file && m.line) {
                                const ideUri = `antigravity://file${m.file}:${m.line}`;
                                window.open(ideUri, "_self");
                              }
                            }}
                            title={`${m.file}:L${m.line}`}
                          >
                            📍
                          </button>
                        </div>
                      ))
                    ) : (
                      <div className="validation-ok">✅ 素材完整</div>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </aside>
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
