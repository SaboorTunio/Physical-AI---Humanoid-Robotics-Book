import React from 'react';
import styles from './ChapterHeader.module.css';

export interface ChapterHeaderProps {
  chapterNumber: number;
  title: string;
  description: string;
  module: number;
  estimatedTime?: number;
  objectives: string[];
  prerequisites?: number[];
  keywords?: string[];
}

export const ChapterHeader: React.FC<ChapterHeaderProps> = ({
  chapterNumber,
  title,
  description,
  module,
  estimatedTime = 45,
  objectives,
  prerequisites = [],
  keywords = [],
}) => {
  const moduleNames = [
    'Foundations',
    'The Body',
    'The Brain',
    'Humanoid Control',
  ];

  return (
    <div className={styles.header}>
      <div className={styles.breadcrumb}>
        <span className={styles.badge}>Module {module}: {moduleNames[module - 1]}</span>
        <span className={styles.chapterLabel}>Chapter {chapterNumber}</span>
      </div>

      <h1 className={styles.title}>{title}</h1>

      <p className={styles.description}>{description}</p>

      <div className={styles.meta}>
        <div className={styles.metaItem}>
          <span className={styles.metaIcon}>⏱️</span>
          <span className={styles.metaText}>{estimatedTime} mins</span>
        </div>
        <div className={styles.metaItem}>
          <span className={styles.metaIcon}>📚</span>
          <span className={styles.metaText}>{objectives.length} Learning Objectives</span>
        </div>
        {keywords.length > 0 && (
          <div className={styles.metaItem}>
            <span className={styles.metaIcon}>🏷️</span>
            <span className={styles.metaText}>{keywords.length} Topics</span>
          </div>
        )}
      </div>

      <div className={styles.content}>
        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>What You'll Learn</h3>
          <ul className={styles.objectivesList}>
            {objectives.map((objective, index) => (
              <li key={index} className={styles.objectiveItem}>
                <span className={styles.checkmark}>✓</span>
                <span>{objective}</span>
              </li>
            ))}
          </ul>
        </div>

        {prerequisites.length > 0 && (
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Prerequisites</h3>
            <div className={styles.prerequisites}>
              <p className={styles.prerequisiteText}>
                Before starting this chapter, make sure you're familiar with:
              </p>
              <ul className={styles.prerequisitesList}>
                {prerequisites.map((chapter) => (
                  <li key={chapter} className={styles.prerequisiteItem}>
                    Chapter {chapter}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {keywords.length > 0 && (
          <div className={styles.section}>
            <h3 className={styles.sectionTitle}>Key Topics</h3>
            <div className={styles.keywords}>
              {keywords.map((keyword, index) => (
                <span key={index} className={styles.keyword}>
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
